# Generated by Django 2.2.24 on 2023-05-31 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("surveys23", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="nosalaryhire",
            name="avg_work_day",
            field=models.FloatField(
                blank=True, null=True, verbose_name="Average Work Day"
            ),
        ),
    ]
