# sender userinfo api
# sender could be client(regular user) or admin
import uuid
from functools import lru_cache
from typing import List

from lib.api.v1.admin.user import IUserInfo, IAdminInfo
from lib.db.postgres import NotificationsDb
from lib.model.user import User

from lib.config import config
from lib.logger import get_logger

logger = get_logger('Sender UserInfo Service')

class AdminUserInfo(IAdminInfo):
    '''User database access through elevated user in django'''
    def __init__(self):
        self.users = []

    def get_admin_user(self, groups):
        return User(**{
            'id': uuid.uuid4(),
            'name': config.notifications.db_user,
            'email': config.notifications.from_email,
            'groups': 'admin,' + groups
        })

    def connect(self):
        self.admin = self.get_admin_user('all')
        self.users.append(self.admin)
        self.manager = self.get_admin_user('all,weekly,manager')
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


@lru_cache()
def get_userinfo() -> IUserInfo:
    '''Production userinfo direct interface through db adapter'''
    return NotificationsDb(
        user=config.notifications.db_user,
        password=config.notifications.db_password,
        host=config.notifications.db_host,
        port=config.notifications.db_port,
        db_name=config.notifications.db_name
    )

@lru_cache()
def get_admin_userinfo() -> IAdminInfo:
    return AdminUserInfo()