import argparse
import json

from functools import partial

from more_itertools import chunked
from pydantic import ValidationError

from lib.api.v1.admin.user import IUserInfo
from lib.db.postgres import NotificationsDb
from lib.db.rabbitmq import RabbitMQ

from lib.service.admin import AdminUserInfo
from lib.service.messages import get_realtime_queue, get_background_queue
from lib.service.notifications import get_notifications
from lib.model.message import Message, MessageChunk, Context, MessageBase

from src.worker.workers.base import BaseWorker

from lib.config import config
from lib.logger import get_logger

logger = get_logger(__name__)

class UserChunkerWorker(BaseWorker):
    def __init__(
            self,
            name: str,
            rabbit_consumer: RabbitMQ,
            rabbit_producer: RabbitMQ,
            userinfo: IUserInfo,
    ):
        super().__init__(name, queuein=rabbit_consumer, queueout=rabbit_producer)
        self.db: IUserInfo = userinfo

    def prepare(self):
        super().prepare()
        self.db.connect()

    @staticmethod
    def generate_message(count_users, func_chunk, payload, message_base):
        output_chunk_size = 0
        for users in func_chunk():
            output_chunk_size += len(users)
            
            # create individual user contexts
            context = Context(payload=payload, users_id=users, group_id=None)
            new_message = Message(**message_base.dict(), context=context)

            if output_chunk_size >= count_users:
                new_message.last_chunk = True
            yield new_message

    def chunk_group_to_users(self, group_id):
        offset = 0
        while True:
            result = self.db.get_users_from_group(group_id, config.notifications.chunk_size, offset)
            list_user = [user.id for user in result]
            yield list_user

            if len(list_user) < config.notifications.chunk_size:
                break
            offset += config.notifications.chunk_size

    def handler(self, ch, method, properties, body):
        body = BaseWorker.load_json_data(body)
        rabbit_message = MessageChunk(**body)

        ch.basic_ack(delivery_tag=method.delivery_tag)

        message_base = MessageBase(**rabbit_message.dict())
        group_id = rabbit_message.context.group_id

        if rabbit_message.context.users_id:
            # case 1: users ids specified directly from admin, in-message
            chunk_users = partial(chunked, rabbit_message.context.users_id, config.notifications.chunk_size)
            count_users = len(rabbit_message.context.users_id)
        elif group_id:
            # case 2: group name provided - send to groups
            chunk_users = self.chunk_group_to_users(group_id)
            count_users = self.db.get_count_users_in_group(group_id)

        for new_message in self.generate_message(
                count_users,
                chunk_users,
                rabbit_message.context.payload,
                message_base,
        ):
            logger.info(' [Produced]: ' + new_message)
            self.queueout.publish_channel(json.dumps(new_message.dict()))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--realtime", action='store_true', help="send to realtime mailer or background queue for further enrich, default true")
    parser.set_defaults(realtime=True)
    
    parser.add_argument("--background", action='store_true', help="send to background queue for further enrich, default false")
    parser.set_defaults(background=False)

    args = parser.parse_args()
    send_to: RabbitMQ = None

    if args.realtime:
        send_to = get_realtime_queue()
    elif args.background:
        send_to = get_background_queue()

    if config.is_development():
        userapi: IUserInfo = AdminUserInfo()
    if config.is_production():
        userapi: IUserInfo = get_notifications()

    # chunker that enriches background tasks and passes them to realtime
    worker: BaseWorker = UserChunkerWorker(
        name='Worker Chunker',
        rabbit_consumer=get_background_queue(),
        rabbit_producer=send_to,
        iuserinfo=userapi,
    )
    worker.run()
