# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-13 22:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainAPP', '0018_auto_20170908_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='zimeiti_article',
            name='user_img',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='zimeiti_article',
            name='user_name',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
