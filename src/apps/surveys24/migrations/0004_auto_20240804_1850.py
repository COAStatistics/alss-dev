# Generated by Django 2.2.24 on 2024-08-04 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys24', '0003_auto_20240720_1829'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stratify',
            name='management_type',
        ),
        migrations.AddField(
            model_name='stratify',
            name='agg_management_type',
            field=models.ManyToManyField(related_name='stratifies', to='surveys24.ManagementType', verbose_name='Management Type'),
        ),
    ]