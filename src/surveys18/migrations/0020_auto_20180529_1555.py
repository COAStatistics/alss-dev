# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-29 07:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys18', '0019_farmrelatedbusiness_has_extra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmrelatedbusiness',
            name='has_business',
            field=models.BooleanField(default=True, verbose_name='Has Business'),
        ),
    ]