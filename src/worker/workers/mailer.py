# Этот файл содержит функции службы отправки Email-нотификаций

from pydantic import ValidationError

from lib.api.v1.admin.notification import INotification
from lib.api.v1.admin.user import IUserInfo
from lib.api.v1.generator.template import ITemplate
from lib.api.v1.sender.email import IEmail
from lib.config import config
from lib.db.rabbitmq import RabbitMQ
from lib.logger import get_logger
from lib.model.message import Message
from lib.service.admin import AdminNotifications, AdminUserInfo
from lib.service.jinja import get_templates
from lib.service.messages import get_realtime_queue
from lib.service.notifications import get_notifications
from lib.service.smtp import EmailSMTPService
from src.generator.enricher import EnrichService
from src.worker.service.policy import PolicyService
from src.worker.workers.base import BaseWorker

logger = get_logger(__name__)


class MailerWorker(BaseWorker):
    """Email notifications sender process"""

    def __init__(
        self,
        name: str,
        iemail: IEmail,
        itemplate: ITemplate,
        iuserinfo: IUserInfo,
        inotification: INotification,
        queuein: RabbitMQ,
    ):
        super().__init__(self, name, queuein=queuein)

        self.mailer: IEmail = iemail
        self.userinfo: IUserInfo = iuserinfo
        self.templater: ITemplate = itemplate
        self.notifier: INotification = inotification

        self.enricher: EnrichService = EnrichService(self.templater)
        self.policer: PolicyService = PolicyService(self.notifier)

    def prepare(self):
        super().prepare()

        self.mailer.connect()
        self.userinfo.connect()
        self.templater.connect()
        self.notifier.connect()

    def handler(self, channel, method, properties, body):
        super().handler(channel, method, properties, body)

        try:
            message_rabbit: Message = Message(**body)
        except ValidationError:
            raise ValueError("Error: corrupted structure message received")

        template = self.templater.get_template(message_rabbit.template_id)
        if not template:
            channel.basic_ack(delivery_tag=method.delivery_tag)
            raise ValueError("No Template to render in email")

        notification = self.notifier.get_notification(message_rabbit.notification_id)
        if not notification:
            channel.basic_ack(delivery_tag=method.delivery_tag)
            raise ValueError("No Notification config found, can not check policy")

        # acknowledge processing
        channel.basic_ack(delivery_tag=method.delivery_tag)

        # send to each user in message batch
        for user_id in message_rabbit.context.users_id:
            user = self.userinfo.get_user(user_id)

            if not self.policer.check_unified_policy(user, notification):
                continue
            message_body = self.enricher.render_personalized(
                template,
                message_rabbit.context.payload.dict(),
                {
                    "username": user.name,
                    "usermail": user.email,
                    "usertimezone": user.timezone,
                },
            )
            try:
                logger.info("Attempt to send rendered: ", message_body)
                self.mailer.send(
                    address=user.email,
                    body=message_body,
                    subject=template.head,
                    sender=self.name,
                )
            except Exception as e:
                logger.error(
                    "Error send message to {}, message: {}".format(user.email, e)
                )
                continue


if __name__ == "__main__":
    # start smtp mailer service
    mailer: IEmail = EmailSMTPService(
        host=config.notifications.mailhog_host,
        port=config.notifications.mailhog_port,
    )

    templater: ITemplate = get_templates()
    input_queue: RabbitMQ = get_realtime_queue()

    if config.is_development():
        userapi: IUserInfo = AdminUserInfo()
        notifications: INotification = AdminNotifications()

    if config.is_production():
        userapi: IUserInfo = get_notifications()
        notifications: INotification = get_notifications()

    worker: BaseWorker = MailerWorker(
        name=config.notifications.from_email,
        iemail=mailer,
        itemplate=templater,
        iuserinfo=userapi,
        inotification=notifications,
        queuein=input_queue,
    )
    worker.run()
