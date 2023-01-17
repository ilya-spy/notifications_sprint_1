import pytz
from django.db import models
from django.utils.translation import gettext_lazy as _
from notifications.models.base import IDModel

TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))


class UserGroup(IDModel):
    name = models.CharField(_("name"), max_length=255)

    class Meta:
        db_table = 'notifications"."user_group'


class UserGroupThrough(IDModel):
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    user_group = models.ForeignKey("UserGroup", on_delete=models.CASCADE)

    class Meta:
        db_table = 'notifications"."user_group_through'


class CustomUser(IDModel):
    name = models.CharField(_("name"), max_length=255)
    email = models.CharField(_("email"), max_length=255)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default="UTC")
    user_group = models.ManyToManyField("UserGroup", through=UserGroupThrough)

    class Meta:
        db_table = 'notifications"."custom_user'


class UserTemplate(IDModel):
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    template = models.ForeignKey("Template", on_delete=models.CASCADE)

    class Meta:
        db_table = 'notifications"."user_template'


class TemplateUserGroup(IDModel):
    user_group = models.ForeignKey("UserGroup", on_delete=models.CASCADE)
    template = models.ForeignKey("Template", on_delete=models.CASCADE)

    class Meta:
        db_table = 'notifications"."template_user_group'


class NotificationUserGroup(IDModel):
    user_group = models.ForeignKey("UserGroup", on_delete=models.CASCADE)
    notification = models.ForeignKey("Notification", on_delete=models.CASCADE)

    class Meta:
        db_table = 'notifications"."notification_user_group'


class UserNotification(IDModel):
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    notification = models.ForeignKey("Notification", on_delete=models.CASCADE)

    class Meta:
        db_table = 'notifications"."user_notification'
