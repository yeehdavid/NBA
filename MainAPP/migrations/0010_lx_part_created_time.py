# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-27 04:52
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainAPP', '0009_lx_created_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='lx_part',
            name='created_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
