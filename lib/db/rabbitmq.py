# класс-синглтон контроллер для рэббит кластера
# библиотечные функции управления, чтения, записи в рэббит

import backoff
import pika

from config import config
from logger import get_logger

logger = get_logger(__name__)


class RabbitMQ:
    def __init__(self, host, user, password, queue, exchange, extype, durable):
        self.host = host
        self.user = user
        self.password = password
        credentials = pika.PlainCredentials(self.user, self.password)

        self.parameters = pika.ConnectionParameters(host=self.host, credentials=credentials)
        self.connection = None
        self.channel = None
        self.queue = queue
        self.exchange = exchange
        self.extype = extype
        self.durable = durable

    @backoff.on_exception(backoff.expo, pika.exceptions.AMQPConnectionError)
    def connect(self):
        if not self.connection:
            logger.info(f'RabbitMQ: trying channel={self.channel}, queue={self.queue}')
            self.connection = pika.BlockingConnection(self.parameters)
            self.channel = self.connection.channel()

            self.init_channel(self)
        logger.info(f'RabbitMQ: connected channel={self.channel}, queue={self.queue}')


    def init_channel(self):
        self.channel.exchange_declare(
            exchange=self.exchange,
            exchange_type=self.extype,
            durable=self.durable,
        )
        self.channel.queue_declare(queue=self.queue, durable=self.durable)
        self.channel.queue_bind(queue=self.queue, exchange=self.exchange)

    def listen_channel(self, handler, auto_ack=True):
        self.channel.basic_consume(queue=self.queue, on_message_callback=handler, auto_ack=auto_ack)

        logger.debug(f' [*] Channel {self.channel} started. Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def publish_channel(self, message):
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.queue,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        logger.debug(' [*] Channel %s: Sent %r' % self.channel, message)