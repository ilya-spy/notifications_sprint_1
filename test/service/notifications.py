# fake controller used to provide mock model services for testing
import uuid
from typing import List

from faker import Faker

from lib.api.v1.admin.notification import INotification
from lib.api.v1.generator.template import ITemplate

from lib.model.notification import Notification
from lib.service.jinja import get_templates

from lib.logger import get_logger

fake = Faker()
logger = get_logger('Fake Notifications Service')


class FakeNotifications(INotification):
    def __init__(self):
        self.notifications = []
        self.weekly_template = get_templates().get_template('weekly')
        self.personal_template = get_templates().get_template('reaction')


    def get_fake_weekly(self, groups):
        return Notification(**{
            'id': uuid.uuid4(),
            'name': fake.name(),
            'type': 'fake',
            'groups': 'weekly',
            'template_id': self.weekly_template.id
        })
        
    def get_fake_personal(self, groups):
        return Notification(**{
            'id': uuid.uuid4(),
            'name': fake.name(),
            'type': 'fake',
            'groups': 'all',
            'template_id': self.personal_template.id
        })

    def connect(self) -> None:
        self.fake_personal = self.get_fake_personal()
        self.notifications.append(self.fake_personal)
        
        self.fake_weekly = self.get_fake_weekly()
        self.notifications.append(self.fake_weekly)

    def get_notification(self, name: str) -> Notification:
        if name == 'personal':
            return self.fake_personal
        if name == 'weekly':
            return self.fake_weekly

    def get_target_groups(self, notification: Notification) -> List[str]:
        return 'test,fake'
