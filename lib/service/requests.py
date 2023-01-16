import http

import requests

from requests import Session

from lib.api.v1.admin.user import IUserInfo
from lib.model.user import User


class UserController(IUserInfo):
    '''User information service requests proxy'''
    def __init__(self, base_url):
        self.base_url = base_url
        self.session: Session = None

    def connect(self):
        if not self.session:
            self.session = Session()

    def get_user(self, uuid):
        url = '{}/user'.format(self.base_url)
        data = {
            'user_id': uuid
        }
        result = self.session.post(url, data=data)

        if result.status_code != http.HTTPStatus.OK:
            raise ValueError(result)
        return User(**result)
