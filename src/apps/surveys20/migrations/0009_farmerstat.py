# Generated by Django 2.2.14 on 2020-08-22 12:45

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ("surveys20", "0008_auto_20200815_2044"),
    ]

    operations = [
        migrations.CreateModel(
            name="FarmerStat",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "create_time",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="Create Time",
                    ),
                ),
                (
                    "update_time",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="Update Time",
                    ),
                ),
                (
                    "stratify",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="farmer_stats",
                        to="surveys20.Stratify",
                        verbose_name="Stratify",
                    ),
                ),
                (
                    "survey",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="farmer_stat",
                        to="surveys20.Survey",
                        verbose_name="Survey",
                    ),
                ),
            ],
            options={
                "verbose_name": "Farmer Stat",
                "verbose_name_plural": "Farmer Stat",
            },
        ),
    ]
