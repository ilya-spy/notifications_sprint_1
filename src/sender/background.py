# Служба управления отложенными массовыми рассылками
# Cлужба реализует методы для работы FastAPI и WebSocket - управляет настройками рассылок в БД

import logging
from http import HTTPStatus
from logging import config
from time import sleep

from lib.config import config
from lib.model.message import Context, Message
from lib.service.admin import get_admin_user, get_admin_notifications
from lib.service.messages import get_background_queue

from lib.api.v1.admin.notification import INotification
from lib.api.v1.generator.template import ITemplate
from lib.api.v1.admin.user import IUserInfo
from lib.db.rabbitmq import RabbitMQ


def process(queue: RabbitMQ, user: IUserInfo, notifications: INotification):
    try:
        data = [{key: value for key, value in item.items()} for item in notifications]

        for item in data:
            params = item.get('params')
            context = Context(
                group_id=params.get('group_id', None),
                users_id=params.get('users_id', None),
                payload=params.get('payload', {})
            )
            message = Message(
                type_send=item.get('title'),
                context=context,
                template_id=item.get('template_id'),
                notification_id=item.get('id')
            )
            logging.debug(message.dict())
            resp = queue.publish_channel(message.dict())
    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    # Choose Background
    queue = get_background_queue()
    user = get_admin_user()
    notes = get_admin_notifications()

    while True:
        process(queue, user, notes)
        sleep(config.notifications.time_to_restart)