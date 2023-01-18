import pytz
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _
from notifications.models.base import IDModel

TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))


USER_GROUPS = (
    ("all", "All"),
    ("monthly", "Monthly"),
    ("weekly", "Weekly"),
    ("daily", "Daily"),
)


class CustomUser(IDModel):
    name = models.CharField(_("name"), max_length=255)
    email = models.CharField(_("email"), max_length=255)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default="UTC")
    user_group = ArrayField(
        models.CharField(max_length=255, choices=USER_GROUPS, default="all"),
        default=list,
    )

    class Meta:
        db_table = 'notifications"."custom_user'


class UserTemplate(IDModel):
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    template = models.ForeignKey("Template", on_delete=models.CASCADE)

    class Meta:
        db_table = 'notifications"."user_template'


class UserNotification(IDModel):
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    notification = models.ForeignKey("Notification", on_delete=models.CASCADE)

    class Meta:
        db_table = 'notifications"."user_notification'
