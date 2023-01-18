# Этот файл содержит базовый класс и описания функций менеджера рассылок
# Менеджер может иметь наследников: EmailSender, WebPushSender, ...

import json

from lib.db.rabbitmq import RabbitMQ
from lib.logger import get_logger

logger = get_logger(__name__)


class BaseWorker:
    @staticmethod
    def load_json_data(body):
        try:
            return json.loads(body)
        except json.decoder.JSONDecodeError:
            return None

    def __init__(
        self,
        name: str,
        queuein: RabbitMQ = None,
        queueout: RabbitMQ = None,
    ) -> None:
        self.name = name
        self.queuein = queuein
        self.queueout = queueout

    def prepare(self):
        """Pre-startup init and settings"""
        if self.queuein:
            self.queuein.connect()
        if self.queueout:
            self.queueout.connect()

    def run(self):
        """Run worker service process"""
        logger.debug(f"{self.name}: Worker preparing")
        self.prepare()

        logger.debug(f"{self.name}: Worker running")
        while True:
            if self.queuein:
                # worker responsible for ack manually to control delivery
                try:
                    self.queuein.listen_channel(self.handler, auto_ack=False)
                except Exception as e:
                    logger.error(e)

    def handler(self, channel, method, properties, body):
        """Callback for incoming queue triggers"""

        message = BaseWorker.load_json_data(body)
        logger.info(f"{self.name}: Message received: {message}")

        # just pass-thorugh here
        self.queueout.publish_channel(body)
