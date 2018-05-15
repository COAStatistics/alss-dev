# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-15 01:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basefarmers', '0026_auto_20180515_0909'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basefarmer',
            name='is_hire',
        ),
        migrations.AddField(
            model_name='basefarmer',
            name='is_hire',
            field=models.ManyToManyField(blank=True, null=True, related_name='is_hire', to='basefarmers.IsHire', verbose_name='Is Hire'),
        ),
    ]