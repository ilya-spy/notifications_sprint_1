import uuid

from django.http import HttpResponse
from notifications.api.v1 import schemas
from notifications.models import CustomUser, Notification, UserGroup

# Create your views here.


def get_notification(request, id: uuid.UUID):
    q = Notification.objects.get(id)

    if not q:
        return HttpResponse(status=404)

    content = schemas.NotificationSchema(
        id=q.id,
        name=q.name,
        type=q.type,
        groups=[group.name for group in q.groups.all()],
        template_id=q.template.id,
    )

    return HttpResponse(
        status=200, content_type="application/json", content=content.json()
    )


def get_notification_groups(request, id: uuid.UUID):
    q = Notification.objects.get(id)

    if not q:
        return HttpResponse(status=404)

    groups = [
        schemas.UserGroupSchema(id=row.id, name=row.name) for row in q.groups.all()
    ]

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
        user_group=[row.name for row in q.user_group.all()],
    )

    return HttpResponse(
        status=200, content_type="application/json", content=content.json()
    )


def get_user_groups(request, id: uuid.UUID):
    q = CustomUser.objects.get(id)

    if not q:
        return HttpResponse(status=404)

    groups = [
        schemas.UserGroupSchema(id=row.id, name=row.name) for row in q.groups.all()
    ]

    if not groups:
        return HttpResponse(status=204)

    return HttpResponse(status=200, content_type="application/json", content=groups)


def get_user_groups_users(request, id: uuid.UUID):
    q = UserGroup.objects.get(id)

    if not q:
        return HttpResponse(status=404)

    users = [
        schemas.CustomUserSchema(
            id=row.id, name=row.name, email=row.email, timezone=row.timezone
        )
        for row in q.user_set.all()
    ]

    if not users:
        return HttpResponse(status=204)

    return HttpResponse(status=200, content_type="application/json", content=users)


def get_user_groups_users_count(request, id: uuid.UUID):
    q = UserGroup.objects.get(id)

    if not q:
        return HttpResponse(status=404)

    users_count = q.user_set.count()

    return HttpResponse(
        status=200,
        content_type="application/json",
        content={"users_count": users_count},
    )
