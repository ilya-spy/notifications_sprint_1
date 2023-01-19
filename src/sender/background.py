# Служба управления отложенными массовыми рассылками
# Cлужба реализует методы для работы FastAPI и WebSocket - управляет настройками рассылок в БД
from functools import lru_cache

from lib.api.v1.admin.user import IUserInfo, IAdminInfo
from lib.db.rabbitmq import RabbitMQ

from lib.service.userinfo import get_userinfo, get_admin_userinfo
from lib.service.messages import get_background_queue
from src.sender.sender import CommonSender

from lib.config import config
from lib.logger import get_logger

logger = get_logger(__name__)


# Choose Background scenario
queue: RabbitMQ = get_background_queue()

# set background delay
delay: int = config.notifications.time_to_restart

@lru_cache
def get_background_sender() -> CommonSender:
    sender_userapi: IUserInfo = get_userinfo()
    return CommonSender(
        queue=queue,
        userid=None,
        userapi=sender_userapi,
        sleeptime=delay
    )

@lru_cache
def get_admin_background_sender() -> CommonSender:
    sender_userapi: IAdminInfo = get_admin_userinfo()
    return CommonSender(
        queue=queue,
        userid=sender_userapi.get_admin_id(),
        userapi=sender_userapi,
        sleeptime=delay
    )