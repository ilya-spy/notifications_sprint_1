# Общие класс службы провайдера сообщений
# Cлужба реализует методы для работы FastAPI и WebSocket - посылает сообщения и события в очереди
from time import sleep
from typing import List
import uuid

from lib.api.v1.admin.user import IUserInfo
from lib.db.rabbitmq import RabbitMQ

from lib.model.notification import Notification
from lib.model.message import Context, Message
from lib.model.user import User

from lib.logger import get_logger
logger = get_logger(__name__)

class CommonSender():
    '''Common queue messages producer'''
    def __init__(
        self,
        queue: RabbitMQ,
        userid: uuid.UUID,
        userapi: IUserInfo,
        sleeptime: int,
    ) -> None:
        self.queue: RabbitMQ = queue
        self.userapi: IUserInfo = userapi
        self.userid: uuid.UUID = userid
        self.sleeptime: int = sleeptime

    def connect(self):
        self.queue.connect()
        self.userapi.connect()

    def process(self, notifications: List[Notification], payload: dict):
        try:
            for item in notifications:
                note: Notification = item.dict()
                user: User = self.userapi.get_user()

                context = Context(
                    group_id=note.groups,
                    users_id=[self.userid],
                    payload=payload.update({
                        'user_groups': user.groups,
                    })
                ),
                message = Message(
                    type_send=note.type,
                    context=context,
                    template_id=note.template_id,
                    notification_id=note.id,
                )
                logger.debug(message.dict())
                self.queue.publish_channel(message.dict())
                logger.info('Submitted message to queue')
            self.notes = []
        except Exception as e:
            logger.error(e)

    def schedule(self, notes: List[Notification], payload: dict):
        # process sending to queue
        self.process(notes, payload)
        
        # blocking delay further requests here to control sender speed
        sleep(self.sleeptime)
