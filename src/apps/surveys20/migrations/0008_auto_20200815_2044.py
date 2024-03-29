# Generated by Django 2.2.14 on 2020-08-15 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("surveys20", "0007_managementtype_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="Stratify",
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
                ("is_hire", models.BooleanField(verbose_name="Is Hire")),
                (
                    "min_field",
                    models.FloatField(blank=True, null=True, verbose_name="Min Field"),
                ),
                (
                    "max_field",
                    models.FloatField(blank=True, null=True, verbose_name="Max Field"),
                ),
                (
                    "min_revenue",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Min Revenue"
                    ),
                ),
                (
                    "max_revenue",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Max Revenue"
                    ),
                ),
                (
                    "code",
                    models.PositiveIntegerField(db_index=True, verbose_name="Code"),
                ),
                (
                    "population",
                    models.PositiveIntegerField(verbose_name="Population(Statistic)"),
                ),
                (
                    "management_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stratifies",
                        to="surveys20.ManagementType",
                        verbose_name="Management Type",
                    ),
                ),
            ],
            options={
                "verbose_name": "Stratify",
                "verbose_name_plural": "Stratify",
            },
        ),
    ]
