# Generated by Django 4.0.3 on 2022-04-06 20:31

import uuid

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.RunSQL(
            sql="""
                    CREATE SCHEMA content;
                """,
            reverse_sql="DROP SCHEMA content CASCADE",
        ),
        migrations.CreateModel(
            name="FilmWork",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
                ("creation_date", models.DateTimeField(verbose_name="creation_date")),
                (
                    "rating",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                        verbose_name="rating",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("movie", "Movie"), ("tv_show", "TV show")],
                        max_length=255,
                        verbose_name="type",
                    ),
                ),
            ],
            options={
                "verbose_name": "movie",
                "verbose_name_plural": "movies",
                "db_table": 'content"."film_work',
            },
        ),
        migrations.CreateModel(
            name="Genre",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255, verbose_name="name")),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
            ],
            options={
                "verbose_name": "Genre",
                "verbose_name_plural": "Genres",
                "db_table": 'content"."genre',
            },
        ),
        migrations.CreateModel(
            name="Person",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "full_name",
                    models.CharField(max_length=255, verbose_name="full_name"),
                ),
            ],
            options={
                "verbose_name": "person",
                "verbose_name_plural": "person",
                "db_table": 'content"."person',
            },
        ),
        migrations.CreateModel(
            name="PersonFilmWork",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "film_work_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="movies.filmwork",
                    ),
                ),
                (
                    "person_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="movies.person"
                    ),
                ),
            ],
            options={
                "db_table": 'content"."person_film_work',
            },
        ),
        migrations.CreateModel(
            name="GenreFilmWork",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "film_work_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="movies.filmwork",
                    ),
                ),
                (
                    "genre_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="movies.genre"
                    ),
                ),
            ],
            options={
                "db_table": 'content"."genre_film_work',
            },
        ),
        migrations.AddField(
            model_name="filmwork",
            name="genre",
            field=models.ManyToManyField(
                through="movies.GenreFilmWork", to="movies.genre"
            ),
        ),
        migrations.AddField(
            model_name="filmwork",
            name="person",
            field=models.ManyToManyField(
                through="movies.PersonFilmWork", to="movies.person"
            ),
        ),
    ]
