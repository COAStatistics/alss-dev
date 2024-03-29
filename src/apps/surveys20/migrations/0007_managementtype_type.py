# Generated by Django 2.2.14 on 2020-08-15 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("surveys20", "0006_auto_20200815_1750"),
    ]

    operations = [
        migrations.AddField(
            model_name="managementtype",
            name="type",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "Crop"), (2, "Animal")],
                null=True,
                verbose_name="Product Type",
            ),
        ),
        migrations.AddField(
            model_name="managementtype",
            name="stratify_with",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "Field"), (2, "Revenue")],
                null=True,
                verbose_name="Stratify With",
            ),
        ),
    ]
