import http
from abc import ABC, abstractmethod

import requests
from faker import Faker
from requests import Session

from models.models_db import User

fake = Faker()


class ApiUserInfoAbstract(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get_user(self, uuid):
        pass


class ApiUserInfo(ApiUserInfoAbstract):
    def __init__(self, base_url):
        self.base_url = base_url
        self.session: Session = None

    def connect(self):
        if not self.session:
            self.session = requests.Session()

    def get_user(self, uuid):
        url = '{}/user'.format(self.base_url)
        data = {
            'user_id': uuid
        }
        result = self.session.post(url, data=data)
        if result.status_code != http.HTTPStatus.OK:
            raise ValueError(result)
        return User(**result)


class ApiUserInfoFake(ApiUserInfo):

    def get_user(self, uuid):
        return User(**{
            'user_id': uuid,
            'user_name': fake.name(),
            'user_email': fake.email()
        })