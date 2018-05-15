# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-10 09:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basefarmers', '0011_auto_20180510_1707'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Application Content Name')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'ApplicationContent',
                'verbose_name_plural': 'ApplicationContent',
            },
        ),
        migrations.CreateModel(
            name='Subsidy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_subsidy', models.CharField(blank=True, max_length=5, null=True, verbose_name='Is Subsidy')),
                ('number_of_people', models.IntegerField(blank=True, null=True, verbose_name='Number Of People')),
                ('application_time', models.DateField(blank=True, null=True, verbose_name='Application Time')),
                ('remark', models.CharField(blank=True, max_length=100, null=True, verbose_name='Remark')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated')),
                ('application_content', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='application_content', to='basefarmers.ApplicationContent', verbose_name='ApplicationContent')),
                ('basefarmer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='subsidy', to='basefarmers.BaseFarmer', verbose_name='BaseFarmer')),
            ],
            options={
                'verbose_name': 'Subsidy',
                'verbose_name_plural': 'Subsidy',
            },
        ),
    ]