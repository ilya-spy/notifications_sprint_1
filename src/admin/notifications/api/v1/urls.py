from django.urls import path
from notifications.api.v1 import views

urlpatterns = [
    path("notification/<uuid:id>/", views.get_notification),
    path("notification/<uuid:id>/user_groups/", views.get_notification_groups),
    path("user/<uuid:id>/", views.get_user),
    path("user/<uuid:id>/user_groups/", views.get_user_groups),
    path("user_group/<str:group>/users/", views.get_user_groups_users),
    path("user_group/<str:group>/users/count/", views.get_user_groups_users_count),
]
