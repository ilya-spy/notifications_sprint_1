import smtplib
from email.message import EmailMessage

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from lib.api.v1.sender.email import IEmail
from lib.config import config
from lib.logger import get_logger

logger = get_logger(__name__)


class EmailSMTPService(IEmail):
    def __init__(self, host: str, port: int, user: str, passwd: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = passwd
        self.server = None

    def connect(self):
        if self.server is None:
            self.server = smtplib.SMTP(self.host, self.port)

    def send(self, address: str, body: str, subject: str = None, sender: str = None):
        message = EmailMessage()
        message["From"] = sender
        message["To"] = address
        message["Subject"] = subject
        
        message.add_alternative(body, subtype='html')
        self.server.sendmail(self.user or sender, address, message.as_string())

    def close(self):
        if self.server is not None:
            self.server.close()


class EmailSMTPSSLService(EmailSMTPService):
    def __init__(self, host: str, port: int, user: str, password: str):
        super().__init__(host, port)
        self.user = user
        self.password = password

    def connect(self):
        if self.server is None:
            self.server = smtplib.SMTP_SSL(self.host, self.port)
            self.server.login(self.user, self.password)



class EmailSendGrid(IEmail):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.server = None

    def connect(self):
        if self.server is None:
            self.server = SendGridAPIClient(self.api_key)

    def send(self, address: str, body: str, subject: str = None, sender: str = None):
        message = Mail(
            from_email=sender,
            to_emails=address,
            subject=subject,
            html_content=body)

        self.server.send(message)
