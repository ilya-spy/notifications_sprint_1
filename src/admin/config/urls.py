from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("movies-api/", include("movies.api.urls")),
    path("notifications-api/", include("notifications.api.urls")),
] + staticfiles_urlpatterns()
