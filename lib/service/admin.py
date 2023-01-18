# Admin controller used to provide mock model services for testing
import uuid
from typing import List
from functools import lru_cache

from lib.api.v1.admin.user import IUserInfo
from lib.api.v1.admin.notification import INotification

from lib.model.user import User
from lib.model.notification import Notification
from lib.service.jinja import get_templates

from lib.config import config
from lib.logger import get_logger

logger = get_logger('Admin UserInfo Service')


class AdminUserInfo(IUserInfo):
    '''User database for administrators access'''
    def __init__(self):
        self.users = []

    def get_admin_userinfo(self, groups):
        return User(**{
            'id': uuid.uuid4(),
            'name': config.notifications.db_user,
            'email': config.notifications.from_email,
            'groups': 'admin,' + groups
        })

    def connect(self):
        self.admin = self.get_admin_userinfo('all')
        self.users.append(self.admin)

        self.manager = self.get_admin_userinfo('all,weekly,manager')
        self.users.append(self.manager)
        
        logger.info('Admin user service connected')

    def get_user(self, id: User.id) -> User:
        user: User = None

        for user in self.users:
            if id == user.id:
                break
        return user

    def get_admin_id(self):
        return self.admin.id

    def get_user_groups(self, user: User) -> List[str]:
        return user.groups

    def get_users_from_group(self, group_id: str, chunk_size: int, offset: int):
        if group_id == 'admin':
            return self.users
        else:
            return []
    
    def get_count_users_in_group(self, group_id: str):
        group_users = \
            self.get_users_from_group(group_id)
        return len(group_users)



    
class AdminNotifications(INotification):
    '''Notifications data base for administrator access'''
    def __init__(self):
        self.notifications = []
        self.admin_template = get_templates().get_template('admin')
        self.weekly_template = get_templates().get_template('weekly')

        admin_sender: AdminSender = AdminSender(
            queue=queue,
            userid=admin_info.get_admin_id(),
            userapi=admin_info,
            sleeptime=config.notifications.time_to_restart
        )
        admin_sender.connect()
    
    def get_admin_notification(self):
        return Notification(**{
            'id': uuid.uuid4(),
            'name': 'admin',
            'type': 'admin',
            'groups': 'admin',
            'template_id': self.admin_template.id
        })
        
    def get_admin_weekly(self):
        return Notification(**{
            'id': uuid.uuid4(),
            'name': 'admin_weekly',
            'type': 'admin',
            'groups': 'admin,weekly',
            'template_id': self.weekly_template.id
        })
    def connect(self) -> None:
        self.admin = self.get_admin_notification()
        self.notifications.append(self.admin)

        self.admin_weekly = self.get_admin_weekly()
        self.notifications.append(self.admin_weekly)
        
    def get_notification(self, name: str) -> Notification:
        if name == 'admin':
            return self.admin
        if name == 'admin_weekly':
            return self.admin_weekly

    def get_target_groups(self, notification: Notification) -> List[str]:
        return 'admin'

@lru_cache()
def get_admin_notifications() -> INotification:
    return AdminNotifications()

@lru_cache()
def get_admin_userinfo() -> IUserInfo:
    return AdminUserInfo()