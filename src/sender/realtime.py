# Служба управления отложенными массовыми рассылками
# Cлужба реализует методы для работы FastAPI и WebSocket - управляет настройками рассылок в БД
from functools import lru_cache

from lib.api.v1.admin.user import IUserInfo, IAdminInfo
from lib.db.rabbitmq import RabbitMQ
from lib.service.userinfo import get_userinfo, get_admin_userinfo

from lib.service.messages import get_realtime_queue
from src.sender.sender import CommonSender

from lib.logger import get_logger
logger = get_logger(__name__)


# Choose Realtime scenario
queue: RabbitMQ = get_realtime_queue()

# set realtime  delay
delay: int = 0

@lru_cache
def get_realtime_sender(userid) -> CommonSender:
    sender_userapi: IUserInfo = get_userinfo()
    return CommonSender(
        queue=queue,
        userid=userid,
        userapi=sender_userapi,
        sleeptime=delay
    )

@lru_cache
def get_admin_realtime_sender() -> CommonSender:
    sender_userapi: IAdminInfo = get_admin_userinfo()
    return CommonSender(
        queue=queue,
        userid=sender_userapi.get_admin_id(),
        userapi=sender_userapi,
        sleeptime=delay
    )