import uuid

from typing import Optional, Union

from pydantic import BaseSettings, Field


class SentryConfig(BaseSettings):
    dsn: Optional[str]

    class Config:
        env_prefix = "sentry_"


class AuthAPIConfig(BaseSettings):
    address: str = Field(default="http://auth_api:8000/")

    class Config:
        env_prefix = "auth_api_"

class KafkaConfig(BaseSettings):
    host: Optional[str] = Field(default="kafka")
    port: Optional[str] = Field(default="9092")
    instance: Optional[str] = Field(default="kafka:9092")

    batch_size: Optional[str] = Field(default=10000000)
    consumer_group_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    topic: Optional[str] = Field(default="watching_progress")

    class Config:
        env_prefix = "kafka_"

class RabbitConfig(BaseSettings):
    host: str = Field('rabbitmq', env='RABBITMQ_HOST')
    user: str = Field('user', env='RABBITMQ_DEFAULT_USER')
    password: str = Field('pass', env='RABBITMQ_DEFAULT_PASS')

    class Config:
        env_prefix = "rabbitmq_"

class RabbitRealtimeConfig(RabbitConfig):
    exchange: str = Field('send_email', env='RABBIT_SEND_EMAIL_QUEUE_EXCHANGE')
    exchange_type: str = Field('direct', env='RABBIT_SEND_EMAIL_QUEUE_EXCHANGE_TYPE')
    queue: str = Field('send_email', env='RABBIT_SEND_EMAIL_QUEUE')
    durable: str = Field('True', env='RABBIT_SEND_EMAIL_QUEUE_DURABLE')

    class Config:
        env_prefix = "rabbit_send_email_queue"

class RabbitBackgroundConfig(RabbitConfig):
    exchange: str = Field('group_chunk', env='RABBIT_CHUNK_QUEUE_EXCHANGE')
    exchange_type: str = Field('direct', env='RABBIT_CHUNK_QUEUE_EXCHANGE_TYPE')
    queue: str = Field('group_chunk', env='RABBIT_CHUNK_QUEUE')
    durable: str = Field('True', env='RABBIT_CHUNK_QUEUE_DURABLE')

    class Config:
        env_prefix = "rabbit_chink_queue"

class NotificationsConfig(BaseSettings):
    notification_db_host: str = Field('db', env='BACKEND_DB_HOST')
    notification_db_port: int = Field(5432, env='BACKEND_DB_PORT')
    notification_db_user: str = Field('postgres', env='BACKEND_DB_USER')
    notification_db_password: str = Field('1234', env='BACKEND_DB_PASSWORD')
    notification_db_name: str = Field('notification', env='BACKEND_DB_NAME')

    from_email: str = Field('Practix "hello@practix.ru"', env='FROM_EMAIL')
    chunk_size: int = 50

    mailhog_host = 'mailhog_notification'
    mailhog_port = 1025
    mailhog_user = ''
    mailhog_password = ''

class Config(BaseSettings):
    """Настройки приложения."""

    app_name: str = Field(default="notifications")
    app_config: str = Field(default="dev")
    debug: bool = Field(default=True)
    loglevel: str = Field(default="DEBUG")

    kafka: KafkaConfig = KafkaConfig()
    auth_api: AuthAPIConfig = AuthAPIConfig()
    sentry: SentryConfig = SentryConfig()
    
    bg_worker: RabbitRealtimeConfig = RabbitRealtimeConfig()
    rt_worker: RabbitBackgroundConfig = RabbitBackgroundConfig()
    notifications: NotificationsConfig = NotificationsConfig()
    
    def is_development(self) -> bool:
        return self.app_config == 'dev'

    def is_production(self) -> bool:
        return self.app_config == 'prod'

class ProductionConfig(Config):
    """Конфиг для продакшена."""

    debug: bool = False
    app_config: str = "prod"
    chunk_size: int = Field(default=100)


class DevelopmentConfig(Config):
    """Конфиг для девелопмент версии."""

    debug: bool = Field(default=True)
    chunk_size: int = 2


# Choose default config
app_config = Config().app_config

config: Union[ProductionConfig, DevelopmentConfig]
if app_config == "prod":
    config = ProductionConfig()
if app_config == "dev":
    config = DevelopmentConfig()
else:
    raise ValueError("Unknown environment stage")
