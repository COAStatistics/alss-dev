# Generated by Django 2.2.14 on 2020-08-15 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("surveys20", "0005_data_migrate_product_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="loss",
            name="type",
        ),
        migrations.RemoveField(
            model_name="product",
            name="type",
        ),
        migrations.RemoveField(
            model_name="unit",
            name="type",
        ),
        migrations.DeleteModel(
            name="ProductType",
        ),
        migrations.RenameField(
            model_name="loss",
            old_name="new_type",
            new_name="type",
        ),
        migrations.RenameField(
            model_name="product",
            old_name="new_type",
            new_name="type",
        ),
        migrations.RenameField(
            model_name="unit",
            old_name="new_type",
            new_name="type",
        ),
        migrations.AlterField(
            model_name="loss",
            name="type",
            field=models.IntegerField(
                choices=[(1, "Crop"), (2, "Animal")], verbose_name="Product Type"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="type",
            field=models.IntegerField(
                choices=[(1, "Crop"), (2, "Animal")], verbose_name="Product Type"
            ),
        ),
    ]
