
import smtplib
import ssl

from email.message import EmailMessage

from faker import Faker

from lib.api.v1.sender.email import IEmail
from lib.logger import get_logger

fake = Faker()
logger = get_logger("Fake SMTP")

class EmailSMTPFake(IEmail):
    '''Fake SMTP server run in testing and development'''
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
    '''Fake SMTP server'''
    def connect(self, user, password):
        self.host = 'localhost'
        self.port = 9999
        self.user = user
        self.password = password

        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        self.server = smtplib.SMTP(self.host, self.port)

        self.server.starttls(context=context)
        self.server.login(self.user, self.password)
        logger.info(f'FakeSMTP SSL server connected')
