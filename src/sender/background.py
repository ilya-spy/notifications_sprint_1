# Служба управления отложенными массовыми рассылками
# Cлужба реализует методы для работы FastAPI и WebSocket - управляет настройками рассылок в БД
import argparse

from lib.api.v1.admin.notification import IAdminNotification
from lib.api.v1.frontend.notification import IClientNotification
from lib.api.v1.admin.user import IUserInfo, IAdminInfo

from lib.db.rabbitmq import RabbitMQ
from lib.service.admin import get_admin_notifications, get_admin_userinfo
from lib.service.notifications import get_notifications, get_userinfo

from lib.service.messages import get_background_queue
from src.sender.sender import CommonSender


from lib.config import config
from lib.logger import get_logger
logger = get_logger(__name__)


if __name__ == "__main__":
    # Choose Background scenario
    queue: RabbitMQ = get_background_queue()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--admin",
        action="store_true",
        help="whether this sender service admin (flag set) or client (default) api",
    )
    parser.set_defaults(admin=False)
    args = parser.parse_args()

    if args.admin:
        # Set admin user and selection of standard admin templates
        sender_userapi: IAdminInfo = get_admin_userinfo()
        sender: IAdminNotification = get_admin_notifications()
    else:
        sender_userapi: IUserInfo = get_userinfo()
        sender: IClientNotification = get_notifications()
