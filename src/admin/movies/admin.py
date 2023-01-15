from django.contrib import admin

from .models import FilmWork, Genre, GenreFilmWork, PersonFilmWork


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork
    extra = 1
    verbose_name = "Movie genre"


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    extra = 1
    verbose_name = "Movie actors"


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (
        GenreFilmWorkInline,
        PersonFilmWorkInline,
    )
    list_display = (
        "title",
        "type",
        "creation_date",
        "rating",
    )
    list_filter = "type", "creation_date"
    search_fields = ("title",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(PersonFilmWork)
class RoleAdmin(admin.ModelAdmin):
    list_display = "film_work", "person", "role"
    search_fields = (
        "person",
        "film_work",
    )
    list_filter = ("role",)
