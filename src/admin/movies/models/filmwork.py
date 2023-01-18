from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .mixins import TimeStampedMixin, UUIDMixin


class GenreFilmWork(UUIDMixin, TimeStampedMixin, models.Model):
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE)
    film_work = models.ForeignKey("FilmWork", on_delete=models.CASCADE)
    created_at = models.DateTimeField("created_at", auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        indexes = (
            models.Index(fields=["genre", "film_work"], name="film_work_creation_date"),
        )
        constraints = (
            models.constraints.UniqueConstraint(
                fields=["film_work", "genre"],
                include=["created_at"],
                name="unique_film_genre",
            ),
        )


class RoleType(models.TextChoices):
    ACTOR = "actor", _("Actor")
    DIRECTOR = "director", _("Director")
    WRITER = "writer", _("Screenwriter")


class PersonFilmWork(UUIDMixin, TimeStampedMixin, models.Model):
    person = models.ForeignKey(
        "person", on_delete=models.CASCADE, verbose_name=_("person")
    )
    film_work = models.ForeignKey(
        "FilmWork", on_delete=models.CASCADE, verbose_name=_("movie")
    )
    role = models.CharField("role", max_length=255, choices=RoleType.choices)
    created_at = models.DateTimeField("created_at", auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        indexes = (
            models.Index(fields=["person", "film_work"], name="person_film_work_idx"),
        )
        constraints = (
            models.constraints.UniqueConstraint(
                fields=["person", "film_work", "role"],
                include=["person", "film_work"],
                name="unique_person_role_film",
            ),
        )
        verbose_name = _("person")
        verbose_name_plural = _("person")


class FilmWorkType(models.TextChoices):
    MOVIE = "movie", _("Movie")
    TV_SHOW = "tv_show", _("TV show")


class FilmWork(UUIDMixin, TimeStampedMixin, models.Model):
    title = models.CharField(_("title"), max_length=255, blank=False)
    description = models.TextField(_("description"), blank=True, null=True)
    creation_date = models.DateTimeField(_("creation_date"), blank=True, null=True)
    rating = models.FloatField(
        _("rating"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    type = models.CharField(_("type"), max_length=255, choices=FilmWorkType.choices)
    genre = models.ManyToManyField("Genre", through=GenreFilmWork)
    person = models.ManyToManyField("Person", through=PersonFilmWork)
    file_path = models.FileField(_("file"), blank=True, null=True, upload_to="movies/")

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _("movie")
        verbose_name_plural = _("movies")

    def __str__(self):
        return self.title
