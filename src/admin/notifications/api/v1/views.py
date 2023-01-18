import uuid

from django.http import HttpResponse
from notifications.api.v1 import schemas
from notifications.models import CustomUser, Notification

# Create your views here.


def get_notification(request, id: uuid.UUID):
    q = Notification.objects.get(id)

    if not q:
        return HttpResponse(status=404)

    content = schemas.NotificationSchema(
        id=q.id,
        name=q.name,
        type=q.type,
        groups=q.groups,
        template_id=q.template.id,
    )

    return HttpResponse(
        status=200, content_type="application/json", content=content.json()
    )


def get_notification_groups(request, id: uuid.UUID):
    q = Notification.objects.get(id)

    if not q:
        return HttpResponse(status=404)

    groups = q.groups

    if not groups:
        return HttpResponse(status=204)

    return HttpResponse(status=200, content_type="application/json", content=groups)


def get_user(request, id: uuid.UUID):
    q = CustomUser.objects.get(id)

    if not q:
        return HttpResponse(status=404)

    content = schemas.CustomUserSchema(
        id=q.id,
        name=q.name,
        email=q.email,
        timezone=q.timezone,
        user_group=q.groups,
    )

    return HttpResponse(
        status=200, content_type="application/json", content=content.json()
    )


def get_user_groups(request, id: uuid.UUID):
    q = CustomUser.objects.get(id)

    if not q:
        return HttpResponse(status=404)

    groups = q.groups

    if not groups:
        return HttpResponse(status=204)

    return HttpResponse(status=200, content_type="application/json", content=groups)


def get_user_groups_users(request, group: str):
    q = CustomUser.objects.filter(user_group__contains=[group])

    if not q:
        return HttpResponse(status=404)

    users = [
        schemas.CustomUserSchema(
            id=row.id, name=row.name, email=row.email, timezone=row.timezone
        )
        for row in q
    ]

    if not users:
        return HttpResponse(status=204)

    return HttpResponse(status=200, content_type="application/json", content=users)


def get_user_groups_users_count(request, group: str):
    users_count = CustomUser.objects.filter(user_group__contains=[group]).count()

    return HttpResponse(
        status=200,
        content_type="application/json",
        content={"users_count": users_count},
    )
