# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-11 15:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0028_auto_20170311_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apt_test',
            name='startDate',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 12, 15, 51, 29, 498162)),
        ),
    ]