# Generated by Django 4.0.4 on 2022-04-23 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0014_alter_personfilmwork_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="birth_date",
            field=models.DateField(null=True),
        ),
    ]
