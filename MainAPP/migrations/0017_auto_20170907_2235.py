# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-07 22:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainAPP', '0016_auto_20170907_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zimeiti_article',
            name='video_url',
            field=models.CharField(default=0, max_length=200),
        ),
    ]
