# Generated by Django 4.0.3 on 2022-04-09 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="personfilmwork",
            old_name="film_work_id",
            new_name="film_work",
        ),
        migrations.RenameField(
            model_name="personfilmwork",
            old_name="person_id",
            new_name="person",
        ),
    ]
