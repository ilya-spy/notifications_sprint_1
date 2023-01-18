from abc import ABC, abstractmethod
from typing import List

from lib.model.user import User


class IUserInfo(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get_user(self, id: User.id) -> User:
        pass
    
    @abstractmethod
    def get_user_groups(self, user: User) -> List[str]:
        pass

    @abstractmethod
    def get_users_from_group(self, group_id: str, chunk_size: int, offset: int):
        pass
    
    @abstractmethod
    def get_count_users_in_group(group_id: str):
        pass