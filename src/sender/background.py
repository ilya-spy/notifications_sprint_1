# Служба управления отложенными массовыми рассылками
# Cлужба реализует методы для работы FastAPI и WebSocket - управляет настройками рассылок в БД

import logging
from http import HTTPStatus
from logging import config
from time import sleep

from config import TIME_TO_RESTART, LOG_CONFIG
from models import Context, Message
from utils.api_rabbit import api_send_message
from utils.posgres_db import PGNotification

config.dictConfig(LOG_CONFIG)


def process(postgres):
    try:
        result = postgres.get_notification()
        data = [{key: value for key, value in item.items()} for item in result]

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
            resp = api_send_message(message.dict())
            if resp.status_code == HTTPStatus.OK:
                postgres.set_status_processing(item.get('id'))

    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    pg = PGNotification()

    while True:
        process(pg)
        sleep(TIME_TO_RESTART)