from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import datetime
# Create your models here.
class Videos(models.Model):#视频
    def __str__(self):
        return self.title

    created_time = models.DateTimeField(default=datetime.datetime.now, blank=True)
    title = models.CharField(max_length=100)

    url = models.CharField(max_length=500, blank=True)
    img_src = models.CharField(max_length=200, blank=True)

class Board_Videos(models.Model):#头条视频
    def __str__(self):
        return self.title

    created_time = models.DateTimeField(default=datetime.datetime.now, blank=True)
    title = models.CharField(max_length=100)

    url = models.CharField(max_length=500, blank=True)
    img_src = models.CharField(max_length=200, blank=True)

class Latest_News(models.Model):#最新新闻
    def __str__(self):
        return self.title

    created_time = models.DateTimeField(default=datetime.datetime.now, blank=True)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True)
    img_src = models.CharField(max_length=200, blank=True)

class Board_News(models.Model):#头条新闻
    def __str__(self):
        return self.title

    created_time = models.DateTimeField(default=datetime.datetime.now, blank=True)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True)
    img_src = models.CharField(max_length=200, blank=True)

class Lx(models.Model):
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

class Hoop_Latest_News(models.Model):
    def __str__(self):
        return self.title

    created_time = models.DateTimeField(default=datetime.datetime.now, blank=True)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True)

class Hoop_Hot_News(models.Model):
    def __str__(self):
        return self.title
    created_time = models.DateTimeField(default=datetime.datetime.now, blank=True)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True)
