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
    host: str = Field('rabbitmq')
    user: str = Field('user')
    password: str = Field('pass')

    class Config:
        env_prefix = "rabbitmq_"
        env_nested_delimeter = "_"

class RabbitRealtimeConfig(RabbitConfig):
    exchange: str = Field('send_email')
    exchange_type: str = Field('direct')
    queue: str = Field('send_email')
    durable: bool = Field('True')

    class Config:
        env_prefix = "rabbit_send_email_"
        env_nested_delimeter = "_"

class RabbitBackgroundConfig(RabbitConfig):
    exchange: str = Field('group_chunk')
    exchange_type: str = Field('direct')
    queue: str = Field('group_chunk')
    durable: bool = Field('True')

    class Config:
        env_prefix = "rabbit_chunk_"
        env_nested_delimeter = "_"

class NotificationsConfig(BaseSettings):
    db_host: str = Field('db')
    db_port: int = Field(5432)
    db_user: str = Field('postgres')
    db_password: str = Field('1234')
    db_name: str = Field('notification')

    from_email: str = Field('Practix "hello@practix.ru"')
    chunk_size: int = 50
    
    time_to_restart = 60

    mailhog_host = 'mailhog_notification'
    mailhog_port = 1025
    mailhog_user = ''
    mailhog_password = ''

    class Config:
        env_prefix = "notifications_"
        env_nested_delimeter = "_"

class Config(BaseSettings):
    """Настройки приложения."""

    app_name: str = Field(default="notifications")
    app_config: str = Field(default="dev")
    debug: bool = Field(default=True)
    loglevel: str = Field(default="DEBUG")

    class Config:
        env_prefix = "notifications_"
        env_nested_delimeter = "_"

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
