import backoff
import sqlalchemy

from datetime import datetime

from logger import get_logger
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from src.admin.notifications.models import Notification, Template, CustomUser

logger = get_logger(__name__)


class NotificationsDb:
    def __init__(self, host: str, port: int, user: str, password: str, db_name: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name
        self.session = None
        self.engine = None
        self.conn = None

    @backoff.on_exception(backoff.expo, sqlalchemy.exc.OperationalError)
    def connect(self):
        if not self.engine:
            self.engine = create_engine(
                "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}".format(
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port,
                    db=self.db_name,
                ),
                echo=False,
            )
        if not self.conn:
            logger.info("connect db")
            self.conn = self.engine.connect()

        if not self.session:
            self.session = Session(bind=self.engine)
        self.__check_connect()

    def __check_connect(self):
        self.conn.scalar(select(1))

    def get_template(self, id):
        return (
            self.session.query(Template)
            .filter(Template.id == id)
            .first()
        )

    def get_notification(self, id):
        return (
            self.session.query(Notification)
            .filter(Notification.id == id)
            .first()
        )

    def list_admin_notifications(self, id):
        return (
            self.session.query(Template)
            .filter(Template.id == id)
            .first()
        )

    def list_client_notifications(self, id):
        return (
            self.session.query(Notification)
            .filter(Notification.id == id)
            .first()
        )

    def set_status_notification(self, notification_id, status):
        task_notification = self.session.query(Notification).get(notification_id)
        task_notification.send_status = status
        task_notification.updated_at = datetime.now()
        self.session.add(task_notification)
        self.session.commit()

    def get_user(self, user_id):
        return (
            self.session.query(CustomUser)
            .filter(CustomUser.id == user_id)
            .first()
        )

    def get_users_from_group(self, group_id, limit, offset):
        return (
            self.session.query(CustomUser)
            .filter(CustomUser.user_group == group_id)
            .order_by(CustomUser.id)
            .limit(limit)
            .offset(offset)
            .all()
        )

    def get_count_users_in_group(self, group_id):
        return (
            self.session.query(CustomUser)
            .filter(CustomUser.user_group == group_id)
            .count()
        )
