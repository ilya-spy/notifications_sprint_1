# Generated by Django 4.0.3 on 2022-04-11 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0012_alter_personfilmwork_role_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="personfilmwork",
            name="role",
            field=models.CharField(
                choices=[
                    ("actor", "Actor"),
                    ("director", "Director"),
                    ("extras", "Extras"),
                    ("writer", "Screenwriter"),
                ],
                max_length=255,
                verbose_name="role",
            ),
        ),
    ]
