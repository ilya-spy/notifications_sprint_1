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


class Config(BaseSettings):
    """Настройки приложения."""

    app_name: str = Field(default="ugc_gate")
    app_config: str = Field(default="dev")
    debug: bool = Field(default=True)
    loglevel: str = Field(default="DEBUG")

    kafka: KafkaConfig = KafkaConfig()
    auth_api: AuthAPIConfig = AuthAPIConfig()
    sentry: SentryConfig = SentryConfig()

class ProductionConfig(Config):
    """Конфиг для продакшена."""

    debug: bool = False
    app_config: str = "prod"

class DevelopmentConfig(Config):
    """Конфиг для девелопмент версии."""

    debug: bool = Field(default=True)


# Choose default config
app_config = Config().app_config

config: Union[ProductionConfig, DevelopmentConfig]
if app_config == "prod":
    config = ProductionConfig()
if app_config == "dev":
    config = DevelopmentConfig()
else:
    raise ValueError("Unknown environment stage")
