# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-26 13:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MainAPP', '0007_auto_20170723_1623'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lx',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Lx_Part',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=150)),
                ('Belong', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MainAPP.Lx')),
            ],
        ),
    ]
