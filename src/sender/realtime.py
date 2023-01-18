# Служба управления мгновенными точечными рассылками
# Cлужба реализует методы для работы FastAPI - настройка мгновенной доставки уведомлений
# Cлужба реализует методы для работы WebSocket - мгновенная доставка уведомлений с открытием сессии
from time import sleep

from lib.api.v1.admin.notification import INotification
from lib.api.v1.admin.user import IUserInfo
from lib.config import config
from lib.db.rabbitmq import RabbitMQ
from lib.service.admin import get_admin_notifications, get_admin_user
from lib.service.messages import get_realtime_queue
from src.sender.background import process

if __name__ == "__main__":
    # Choose Real time
    queue: RabbitMQ = get_realtime_queue()

    user: IUserInfo = get_admin_user()
    notes: INotification = get_admin_notifications()

    while True:
        process(queue, user, notes)
        sleep(config.notifications.time_to_restart)
