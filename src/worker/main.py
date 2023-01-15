import argparse

from config import Settings
from core.db import NotificationsDb
from core.get_user import ApiUserInfoFake
from core.mail import EmailSMTPMailhog
from core.rabbit import Rabbit
from core.worker import WorkerSendMessage
from functools import partial

settings = Settings()


def init_channel(cls, settings_q):
    cls.channel.exchange_declare(
        exchange=settings_q.exchange,
        exchange_type=settings_q.exchange_type,
        durable=settings_q.durable,
    )

    cls.channel.queue_declare(queue=settings_q.queue, durable=settings_q.durable)
    cls.channel.queue_bind(exchange=settings_q.exchange, queue=settings_q.queue)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--priority", action='store_true', help="priority queue, default false")
    parser.set_defaults(priority=False)

    args = parser.parse_args()

    if args.priority:
        settings_queue = settings.rabbit_send_email_priority
    else:
        settings_queue = settings.rabbit_send_email

    db = NotificationsDb(
        user=settings.notification_db_user,
        password=settings.notification_db_password,
        host=settings.notification_db_host,
        port=settings.notification_db_port,
        db_name=settings.notification_db_name
    )

    email = EmailSMTPMailhog(
        host=settings.mailhog_host,
        port=settings.mailhog_port,
        user=settings.mailhog_user,
        password=settings.mailhog_password,
        from_email=settings.from_email
    )

    rabbit = Rabbit(
        settings.rabbit_host,
        settings.rabbit_user,
        settings.rabbit_password,
        queue=settings_queue.queue,
        exchange=settings_queue.exchange,
        init_channel=partial(init_channel, settings_q=settings_queue)
    )

    api = ApiUserInfoFake('url_fake')

    w = WorkerSendMessage(rabbit, db, email, api)
    w.run()
