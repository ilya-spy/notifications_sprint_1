# fake controller used to provide mock model services for testing
import ssl
import smtplib

from email.message import EmailMessage
from faker import Faker

from lib.api.v1.admin.user import IUserInfo
from lib.api.v1.sender.email import IEmail

from lib.model.user import User

from lib.logger import get_logger

fake = Faker()
logger = get_logger()

class UserControllerFake(IUserInfo):
    def get_user(self, uuid):
        return User(**{
            'user_id': uuid,
            'user_name': fake.name(),
            'user_email': fake.email()
        })


class EmailSMTPFake(IEmail):
    def connect(self):
        logger.info('connect FakeSMTP')

    def send(self, address: str, message: str, subject: str = None, sender: str = None):
        message = EmailMessage()
        message["From"] = sender
        message["To"] = address
        message["Subject"] = subject

        message.add_alternative(message, subtype='html')
        logger.info(f'FakeSMTP message: {message}')

    def close(self):
        logger.info('disconnect FakeSMTP')



class EmailSMTPSSLFake(EmailSMTPFake):
    def connect(self):
        self.host = 'host'
        self.port = 9999

        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        self.server = smtplib.SMTP(self.host, self.port)

        self.server.starttls(context=context)
        self.server.login(self.user, self.password)
        logger.info(f'FakeSMTP SSL server connected')
