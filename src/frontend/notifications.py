
# notifications core backend services
import uuid
from typing import List
from functools import lru_cache

from lib.api.v1.admin.notification import INotification, IAdminNotification
from lib.api.v1.frontend.notification import IClientNotification

from lib.db.postgres import NotificationsDb
from lib.model.notification import Notification
from lib.model.template import Template
from lib.model.user import User

from lib.service.jinja import get_templates

from lib.config import config
from lib.logger import get_logger

from src.generator.enricher import EnrichService
from src.sender.sender import CommonSender
from src.sender.background import get_background_sender, get_admin_background_sender
from src.sender.realtime import get_realtime_sender, get_admin_realtime_sender

logger = get_logger()

logger = get_logger('Notifications Service')


class AdminNotifications(INotification):
    '''Notifications services for administrator access'''
    def __init__(self) -> IAdminNotification:
        self.notifications = []

        self.admin_template = get_templates().get_template('admin')
        self.weekly_template = get_templates().get_template('weekly')

        self.admin_realtime_sender = get_admin_realtime_sender()
        self.admin_background_sender = get_admin_background_sender()

    def connect(self) -> None:
        self.admin_realtime_sender.connect()
        self.admin_background_sender.connect()

        self.admin = self.get_admin_notification('admin', 'admin')
        self.notifications.append(self.admin)

        self.admin_weekly = self.get_admin_notification('admin', 'admin,weekly')
        self.notifications.append(self.admin_weekly)
        
    def get_notification(self, name: str) -> Notification:
        if name == 'admin':
            return self.admin
        if name == 'admin_weekly':
            return self.admin_weekly

    def get_target_groups(self, notification: Notification) -> List[str]:
        return 'admin'

    def get_admin_notification(self, name, groups):
        return Notification(**{
            'id': uuid.uuid4(),
            'name': name,
            'type': 'admin',
            'groups': groups,
            'template_id': self.admin_template.id
        })

    def get_admin_notifications(self) -> List[Notification]:
        return self.notifications

    def send_immediate(self, notification: Notification) -> int:
        self.admin_realtime_sender.schedule([notification])

    def schedule_background(self, notification: Notification) -> int:
        self.admin_background_sender.schedule([notification])


class ClientNotifications(INotification):
    '''Notifications services for client(production) access'''
    def __init__(self) -> IClientNotification:

        self.client_notifications_db =  NotificationsDb(
            user=config.notifications.db_user,
            password=config.notifications.db_password,
            host=config.notifications.db_host,
            port=config.notifications.db_port,
            db_name=config.notifications.db_name
        )
        self.background_sender: CommonSender = get_background_sender()
        self.realtime_sender: CommonSender = get_realtime_sender()

        self.enricher = EnrichService(get_templates(), self.client_notifications_db)

    def connect(self) -> None:
        self.background_sender.connect()
        self.realtime_sender.connect()

    def send_notification(self, note_id: uuid.UUID) -> Notification:
        '''Broadcast message, knowing its note id. Sender policy determine users to send'''
        note: Notification = self.client_notifications_db.get_notification(note_id)
        self.background_sender.schedule([note])

    def user_notification(self, note_id: uuid.UUID, user_id: uuid.UUID) -> Notification:
        '''Send user notification. Sender policy would check/enforce subscription rules'''
        realtime_sender: CommonSender = get_realtime_sender(user_id)
        note: Notification = self.client_notifications_db.get_notification(note_id)

        realtime_sender.schedule([note])
    
    def send_event(self, evnt_type: str):
        '''Notify service of content updates (weekly, daily, ...). Sender policy determine users to send'''
        note: Notification = self.client_notifications_db.get_notification(evnt_type)
        note.groups = 'all'

        self.background_sender.schedule([note])


    def user_event(self, user_id: uuid.UUID, evnt_type: str) -> Notification:
        '''Notify user personal updates. Sender policy would check/enforce subscription rules'''
        note: Notification = self.client_notifications_db.get_notification(evnt_type)
        template: Template = self.client_notifications_db.get_template(note.template_id)
        user: User = self.client_notifications_db.get_user(user_id)
        
        payload = self.enricher.render_personalized(
            template=template,
            context = {
                'userid': user.id,
                'username': user.name,
                'useremail': user.email
            }
        )
        self.realtime_sender.schedule([note], payload)


@lru_cache()
def get_admin_notifications_service() -> IAdminNotification:
    return AdminNotifications()

@lru_cache()
def get_client_notifications_service() -> IClientNotification:
    return ClientNotifications()