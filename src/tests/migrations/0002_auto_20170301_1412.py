# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 14:12
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apt_test',
            name='Duration',
        ),
        migrations.AddField(
            model_name='apt_test',
            name='endDate',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
