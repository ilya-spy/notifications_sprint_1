# класс-синглтон контроллер для рэббит кластера
# библиотечные функции управления, чтения, записи в рэббит

import backoff
import pika

from pika.adapters.blocking_connection import BlockingChannel
from pika.connection import Connection, ConnectionParameters
from pika.exceptions import AMQPConnectionError
from pika.spec import PERSISTENT_DELIVERY_MODE

from lib.model.message import Message, MessageChunk

from logger import get_logger

logger = get_logger(__name__)


class RabbitMQ:
    def __init__(self,
                 host: str,
                 user: str,
                 password:str,
                 queue: str,
                 exchange: str,
                 extype: str,
                 durable: bool):
        self.host: str = host
        self.user: str = user
        self.password: str = password
        credentials: pika.PlainCredentials = pika.PlainCredentials(self.user, self.password)
        self.parameters: ConnectionParameters = ConnectionParameters(host=self.host, credentials=credentials)

        self.connection: Connection = None
        self.channel: BlockingChannel = None
        self.queue: str = queue
        self.exchange: str = exchange
        self.extype :str = extype
        self.durable: bool = durable

    @backoff.on_exception(backoff.expo, AMQPConnectionError)
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

    def listen_channel(self, handler: function, auto_ack=True):
        consumer_tag = self.channel.basic_consume(queue=self.queue, on_message_callback=handler, auto_ack=auto_ack)

        logger.debug(f' [*] Channel {self.channel} started. Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()
        return consumer_tag

    def publish_channel(self, message: Message):
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.queue,
            body=message.dict(),
            properties=pika.BasicProperties(
                delivery_mode=PERSISTENT_DELIVERY_MODE
            ))
        logger.debug(' [*] Channel %s: Sent %r' % self.channel, message)
