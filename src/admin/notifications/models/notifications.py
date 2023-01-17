from django.db import models
from django.utils.translation import gettext_lazy as _
from notifications.models import base, users


class Notification(base.IDModel):
    name = models.CharField(_("name"), max_length=256)
    type = models.CharField(_("type"), max_length=256)
    template = models.ForeignKey("Template", on_delete=models.CASCADE)
    user = models.ManyToManyField("CustomUser", through=users.UserNotification)
    user_group = models.ManyToManyField(
        "UserGroup", through=users.NotificationUserGroup
    )

    class Meta:
        db_table = 'notifications"."notifications'
