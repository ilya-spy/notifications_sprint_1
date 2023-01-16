# Этот файл содержит функции службы отправки Email-нотификаций

from more_itertools import chunked
from pydantic import ValidationError

from lib.api.v1.admin.user import IUserInfo
from lib.config import config #NotificationStatus, Settings
from lib.db.postgres import NotificationsDb
from lib.db.rabbitmq import RabbitMQ
from lib.logger import get_logger

from src.worker.workers.base import BaseWorker
from src.worker.enrich import EnrichService

from core.mail import AbstractEmail
from core.rabbit import Rabbit
from models.message import Message, MessageChunk, Context, MessageBase

logger = get_logger(__name__)


class MailerWorker(BaseWorker):
    '''Email notifications sender process'''

    def __init__(
            self,
            email: EmailAPI,
            queue: RabbitMQ,
            user: IUserInfo,
            template: GeneratorAPI
    ):
        super().__init__(self, 'MailerWorker', queue)
        self.mailer = mailer
        self.userapi = userapi
        self.template
        self.enricher = EnrichService(self.userapi)


    def prepare(self):
        super().prepare()
        self.mailer.connect()

    def handler(self, channel, method, properties, body):
        super().handler(channel, method, properties, body)

        try:
            message_rabbit = Message(**body)
        except ValidationError as e:
            raise ValueError('Error structure message')


        if not template_raw:
            channel.basic_ack(delivery_tag=method.delivery_tag)
            raise ValueError('Not Template')

        type_notification = template_raw.TypeNotification
        template = template_raw.Template

        unsubscribe_user = [item.user_id for item in self.db.get_unsubscribe(
            type_notification.title,
            users_id=message_rabbit.context.users_id
        )]
        channel.basic_ack(delivery_tag=method.delivery_tag)

        for user_id in message_rabbit.context.users_id:
            if user_id in unsubscribe_user:
                continue
            user_info = self.api_user.get_user(user_id)
            context_user = {**message_rabbit.context.payload.dict(), 'username': user_info.user_name}
            message = self.__template_render(template.code, context_user)
            try:
                self.email.send(template.subject, user_info.user_email, message)
            except Exception as e:
                logger.error('Error send message to {}, message: {}'.format(user_info, e))

        if message_rabbit.notification_id and message_rabbit.last_chunk:
            self.db.set_status_notification(message_rabbit.notification_id, NotificationStatus.done.value)

    def run(self):
        run_worker(self, self.rabbit)
