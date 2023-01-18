from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _
from notifications.models import base, users


class Template(base.IDModel, base.BaseModel):
    name = models.CharField(_("name"), max_length=255)
    head = models.TextField(_("head"))
    body = models.TextField(_("head"))
    user_group = ArrayField(
        models.CharField(max_length=255, choices=users.USER_GROUPS, default="all"),
        default=list,
    )
