import argparse

from lib.config import config

from core.get_user import ApiUserInfoFake
from core.mail import EmailSMTPMailhog
from core.rabbit import Rabbit
from core.worker import WorkerSendMessage
from functools import partial



if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--priority", action='store_true', help="priority queue, default false")
    parser.set_defaults(priority=False)

    args = parser.parse_args()

    if args.priority:
        settings_queue = settings.rabbit_send_email_priority
    else:
        settings_queue = settings.rabbit_send_email


    email = EmailSMTPMailhog(
        host=settings.mailhog_host,
        port=settings.mailhog_port,
        user=settings.mailhog_user,
        password=settings.mailhog_password,
        from_email=settings.from_email
    )



    if config.app_config == 'dev':
        api = ApiUserInfoFake('url_fake')

    w = WorkerSendMessage(rabbit, db, email, api)
    w.run()
