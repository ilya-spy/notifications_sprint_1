from abc import ABC, abstractmethod

from lib.model.user import User


class IUserInfo(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get_user(self, uuid: User.user_id):
        pass
