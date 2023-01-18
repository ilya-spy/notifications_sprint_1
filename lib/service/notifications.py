
# notifications core backend services
from functools import lru_cache

from lib.api.v1.admin.user import IUserInfo
from lib.api.v1.admin.notification import INotification
from lib.api.v1.generator.template import ITemplate

from lib.db.postgres import NotificationsDb

from lib.config import config
from lib.logger import get_logger

logger = get_logger()

@lru_cache()
def get_userinfo() -> IUserInfo:
    '''Production userinfo db'''
    return NotificationsDb(
        user=config.notifications.notification_db_user,
        password=config.notifications.notification_db_password,
        host=config.notifications.notification_db_host,
        port=config.notifications.notification_db_port,
        db_name=config.notifications.notification_db_name
    )

@lru_cache()
def get_notifications() -> INotification:
    '''Production notifications db'''
    return NotificationsDb(
        user=config.notifications.notification_db_user,
        password=config.notifications.notification_db_password,
        host=config.notifications.notification_db_host,
        port=config.notifications.notification_db_port,
        db_name=config.notifications.notification_db_name
    )

