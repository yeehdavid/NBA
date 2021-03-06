# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-08 20:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainAPP', '0017_auto_20170907_2235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zimeiti_img',
            name='belong',
        ),
        migrations.AddField(
            model_name='zimeiti_article',
            name='img_count',
            field=models.CharField(default=0, max_length=50),
        ),
        migrations.AddField(
            model_name='zimeiti_article',
            name='img_src_1',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='zimeiti_article',
            name='img_src_2',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='zimeiti_article',
            name='img_src_3',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='zimeiti_article',
            name='img_src_4',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='zimeiti_article',
            name='img_src_5',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='zimeiti_article',
            name='img_src_6',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='zimeiti_article',
            name='img_src_7',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='zimeiti_article',
            name='img_src_8',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='zimeiti_article',
            name='img_src_9',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='zimeiti_article',
            name='url',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.DeleteModel(
            name='ZiMeiTi_Img',
        ),
    ]
