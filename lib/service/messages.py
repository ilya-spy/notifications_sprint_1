# message queue router services
from functools import lru_cache

from lib.db.rabbitmq import RabbitMQ

from lib.config import config
from lib.logger import get_logger

logger = get_logger()

@lru_cache()
def get_realtime_queue():
    return RabbitMQ(
        config.rt_worker.host,
        config.rt_worker.user,
        config.rt_worker.password,
        queue=config.rt_worker.queue,
        exchange=config.rt_worker.exchange,
        extype=config.rt_worker.exchange_type,
        durable=config.rt_worker.durable
    )

@lru_cache()
def get_background_queue():
    return RabbitMQ(
        config.bg_worker.host,
        config.bg_worker.user,
        config.bg_worker.password,
        queue=config.bg_worker.queue,
        exchange=config.bg_worker.exchange,
        extype=config.bg_worker.exchange_type,
        durable=config.bg_worker.durable
    )
