from django.urls import path

from . import views

urlpatterns = [
    path("movies/<uuid:id>/", views.DetailedMovieApi.as_view()),
    path("movies/", views.ListMoviesApi.as_view()),
]
