# Этот файл содержит базовый класс и описания функций менеджера рассылок
# Менеджер может иметь наследников: EmailSender, WebPushSender, ...

import json
import logging
from functools import partial

from more_itertools import chunked
from pydantic import ValidationError

from config import LOGGING_CONFIG, NotificationStatus, Settings
from core.db import NotificationsDb
from core.get_user import ApiUserInfoAbstract
from core.mail import AbstractEmail
from core.rabbit import Rabbit
from models.message import Message, MessageChunk, Context, MessageBase

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

settings = Settings()


def run_worker(cls, rabbit):
    pass


def decode_data_from_json(body):
    try:
        return json.loads(body)
    except json.decoder.JSONDecodeError as exc:
        return None


class BaseWorker():

    def prepare(self):
        pass

    def run(self):
        logger.debug('[BaseWorker]: run')

        while True:
            cls.all_connect_dependencies()
            try:
                rabbit.listen_channel(cls.callback, auto_ack=False)
            except Exception as e:
                logger.error(e)

    def callback(self):
        pass


class WorkerSendMessage(WorkerAbstract):
    def __init__(
            self,
            rabbit_notification: Rabbit,
            db_notification: NotificationsDb,
            email_notification: AbstractEmail,
            api: ApiUserInfoAbstract,
    ):
        self.db = db_notification
        self.rabbit = rabbit_notification
        self.email = email_notification
        self.api_user = api

    def all_connect_dependencies(self):
        self.db.connect()
        self.rabbit.connect()
        self.email.connect()

    @staticmethod
    def __template_render(template, context=None):
        if not context:
            context = {}
        template = Template(template)
        return template.render(context)

    def callback(self, ch, method, properties, body):
        body = decode_data_from_json(body)
        try:
            message_rabbit = Message(**body)
        except ValidationError as e:
            raise ValueError('Error structure message')
        template_raw = self.db.get_template(message_rabbit.template_id)

        if not template_raw:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            raise ValueError('Not Template')

        type_notification = template_raw.TypeNotification
        template = template_raw.Template

        unsubscribe_user = [item.user_id for item in self.db.get_unsubscribe(
            type_notification.title,
            users_id=message_rabbit.context.users_id
        )]
        ch.basic_ack(delivery_tag=method.delivery_tag)

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


class WorkerChunkUserFromGroup(WorkerAbstract):
    def __init__(
            self,
            rabbit_consumer: Rabbit,
            rabbit_publish: Rabbit,
            db_notification: NotificationsDb,
    ):
        self.db = db_notification
        self.rabbit_consumer = rabbit_consumer
        self.rabbit_publish = rabbit_publish

    def all_connect_dependencies(self):
        self.db.connect()
        self.rabbit_consumer.connect()
        self.rabbit_publish.connect()

    @staticmethod
    def __generate_message(count_users, func_chunk, payload, message_base):
        count_response_user = 0
        for users in func_chunk():
            count_response_user += len(users)
            context = Context(payload=payload, users_id=users, group_id=None)

            new_message = Message(**message_base.dict(), context=context)
            if count_response_user >= count_users:
                new_message.last_chunk = True
            yield new_message

    def __chunk_group_to_users(self, group_id):
        offset = 0
        while True:
            result = self.db.get_users_from_group(group_id, settings.chunk_size, offset)
            list_user = [user.user_id for user in result]
            yield list_user
            if len(result) < settings.chunk_size:
                break
            offset += settings.chunk_size

    def callback(self, ch, method, properties, body):
        body = decode_data_from_json(body)
        rabbit_message = MessageChunk(**body)

        if rabbit_message.notification_id:
            self.db.set_status_notification(rabbit_message.notification_id, NotificationStatus.processing.value)
        ch.basic_ack(delivery_tag=method.delivery_tag)

        message_base = MessageBase(**rabbit_message.dict())
        group_id = rabbit_message.context.group_id

        chunk_users = partial(chunked, rabbit_message.context.users_id, settings.chunk_size)
        chunk_group = partial(self.__chunk_group_to_users, group_id)

        if rabbit_message.context.users_id:
            count_users = len(rabbit_message.context.users_id)
            chunk_function = chunk_users
        elif group_id:
            count_users = self.db.get_count_users_in_group(group_id)
            chunk_function = chunk_group

        for new_message in self.__generate_message(
                count_users,
                chunk_function,
                rabbit_message.context.payload,
                message_base,
        ):
            logger.info(new_message)
            self.rabbit_publish.publish(json.dumps(new_message.dict()))

    def run(self):
        run_worker(self, self.rabbit_consumer)