# Служба управления мгновенными точечными рассылками
# Cлужба реализует методы для работы FastAPI - настройка мгновенной доставки уведомлений

import argparse

from lib.api.v1.admin.notification import IAdminNotification
from lib.api.v1.frontend.notification import IClientNotification
from lib.api.v1.admin.user import IUserInfo, IAdminInfo

from lib.db.rabbitmq import RabbitMQ
from lib.service.admin import get_admin_notifications, get_admin_userinfo
from lib.service.notifications import get_notifications, get_userinfo

from lib.service.messages import get_realtime_queue
from src.sender.sender import CommonSender

if __name__ == "__main__":
    # Choose Real time
    queue: RabbitMQ = get_realtime_queue()


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