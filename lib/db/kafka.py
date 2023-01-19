# класс-синглтон контроллер для кафка кластера
# библиотечные функции управления, чтения, записи в кафку

import asyncio
from functools import lru_cache

from aiokafka import AIOKafkaProducer  # type: ignore
from aiokafka import AIOKafkaConsumer  # type: ignore

from lib.config import config


@lru_cache
def get_kafka_producer() -> AIOKafkaProducer:
    """Singleton async kafka producer"""
    loop = asyncio.get_event_loop()

    producer = AIOKafkaProducer(
        loop=loop, client_id=config.app_name, bootstrap_servers=[config.kafka.instance]
    )
    return producer


@lru_cache
def get_kafka_consumer() -> AIOKafkaConsumer:
    """Singleton async kafka consumer."""
    consumer = AIOKafkaConsumer(
        config.kafka.watching_progress_topic,
        bootstrap_servers=f"{config.kafka.host}:{config.kafka.port}",
        group_id=config.kafka.consumer_group_id,
        enable_auto_commit=False,
    )
    return consumer