# Generated by Django 4.0.3 on 2022-04-09 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0005_filmwork_file_path"),
    ]

    operations = [
        migrations.AlterField(
            model_name="filmwork",
            name="creation_date",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="creation_date"
            ),
        ),
    ]
