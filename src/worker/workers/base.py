# Этот файл содержит базовый класс и описания функций менеджера рассылок
# Менеджер может иметь наследников: EmailSender, WebPushSender, ...

import json

from lib.config import config
from lib.db.rabbitmq import RabbitMQ
from lib.logger import get_logger

logger = get_logger(__name__)


class BaseWorker():
    @staticmethod
    def load_json_data(body):
        try:
            return json.loads(body)
        except json.decoder.JSONDecodeError as exc:
            return None

    def __init__(
            self,
            name: str,
            queue: RabbitMQ,
    ) -> None:
        self.name = name
        self.queue = queue

    def prepare(self):
        '''Pre-startup init and settings'''
        self.userapi.connect()
        self.queue.connect()

    def run(self):
        '''Run worker service process'''
        logger.debug(f'{self.name}: Worker preparing')
        self.prepare()

        logger.debug(f'{self.name}: Worker running')
        while True:
            try:
                # worker responsible for ack manually to control delivery
                self.queue.listen_channel(self.handler, auto_ack=False)
            except Exception as e:
                logger.error(e)

    def handler(self, channel, method, properties, body):
        '''Callback for incoming queue triggers'''

        body = BaseWorker.load_json_data(body)
        logger.info(f'{self.name}: Message received: {body}')
