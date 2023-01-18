from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _
from notifications.models import base, users

NOTIFICATION_TYPE = (("instant", _("Instant")), ("scheduled", _("Scheduled")))


class Notification(base.IDModel):
    name = models.CharField(_("name"), max_length=256)
    type = models.CharField(
        _("type"), choices=NOTIFICATION_TYPE, default="instant", max_length=256
    )
    template = models.ForeignKey("Template", on_delete=models.CASCADE)
    user = models.ManyToManyField("CustomUser", through=users.UserNotification)
    user_group = ArrayField(
        models.CharField(max_length=255, choices=users.USER_GROUPS, default="all"),
        default=list,
    )

    class Meta:
        db_table = 'notifications"."notifications'
