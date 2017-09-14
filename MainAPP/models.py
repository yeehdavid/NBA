from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import datetime


# Create your models here.
class Videos(models.Model):  # NBA官网视频
    def __str__(self):
        return self.title

    created_time = models.DateTimeField(default=datetime.datetime.now, blank=True)
    title = models.CharField(max_length=100)

    url = models.CharField(max_length=500, blank=True)
    img_src = models.CharField(max_length=200, blank=True)


class Board_Videos(models.Model):  # NBA官网头条视频
    def __str__(self):
        return self.title

    created_time = models.DateTimeField(default=datetime.datetime.now, blank=True)
    title = models.CharField(max_length=100)

    url = models.CharField(max_length=500, blank=True)
    img_src = models.CharField(max_length=200, blank=True)


class Latest_News(models.Model):  # NBA官网最新新闻
    def __str__(self):
        return self.title

    created_time = models.DateTimeField(default=datetime.datetime.now, blank=True)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True)


class Board_News(models.Model):  # NBA官网头条新闻
    def __str__(self):
        return self.title

    created_time = models.DateTimeField(default=datetime.datetime.now, blank=True)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True)
    img_src = models.CharField(max_length=200, blank=True)


class Lx(models.Model):  # 98录像
    def __str__(self):
        return self.title

    title = models.CharField(max_length=100)
    created_time = models.DateTimeField(default=datetime.datetime.now, blank=True)


class Lx_Part(models.Model):
    def __str__(self):
        return self.title

    title = models.CharField(max_length=100)
    url = models.CharField(max_length=150)
    Belong = models.ForeignKey(Lx)
    created_time = models.DateTimeField(default=datetime.datetime.now, blank=True)


class Hoop_Latest_News(models.Model):  # 虎扑最新新闻
    def __str__(self):
        return self.title

    created_time = models.DateTimeField(default=datetime.datetime.now, blank=True)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True)


class Hoop_Hot_News(models.Model):  # 虎扑头条新闻
    def __str__(self):
        return self.title

    created_time = models.DateTimeField(default=datetime.datetime.now, blank=True)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True)


class Jrs(models.Model):
    created_time = models.DateTimeField(default=datetime.datetime.now, blank=True)
    url = models.CharField(max_length=200, blank=True)
    game_tag = models.CharField(max_length=200, blank=True)
    game_time = models.CharField(max_length=200, blank=True)
    first_team_logo = models.CharField(max_length=200, blank=True)
    first_team_name = models.CharField(max_length=200, blank=True)
    second_team_name = models.CharField(max_length=200, blank=True)
    second_team_logo = models.CharField(max_length=200, blank=True)


class ZiMeiTi_Article(models.Model):

    def __str__(self):
        return self.title

    title = models.TextField()
    url = models.CharField(max_length=200, blank=True)
    created_time = models.DateTimeField(default=datetime.datetime.now)

    user_img = models.CharField(max_length=200, blank=True)
    user_name = models.CharField(max_length=200, blank=True)

    video_url = models.CharField(max_length=200, default=0)

    img_src_1 = models.CharField(max_length=200, blank=True)
    img_src_2 = models.CharField(max_length=200, blank=True)
    img_src_3 = models.CharField(max_length=200, blank=True)
    img_src_4 = models.CharField(max_length=200, blank=True)
    img_src_5 = models.CharField(max_length=200, blank=True)
    img_src_6 = models.CharField(max_length=200, blank=True)
    img_src_7 = models.CharField(max_length=200, blank=True)
    img_src_8 = models.CharField(max_length=200, blank=True)
    img_src_9 = models.CharField(max_length=200, blank=True)

    img_count = models.CharField(max_length=50,default=0)
