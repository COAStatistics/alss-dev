# Generated by Django 2.2 on 2019-04-20 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("surveys19", "0005_builderfile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="max_hour",
            field=models.FloatField(blank=True, null=True, verbose_name="Max Hour"),
        ),
        migrations.AlterField(
            model_name="product",
            name="min_hour",
            field=models.FloatField(blank=True, null=True, verbose_name="Min Hour"),
        ),
    ]
