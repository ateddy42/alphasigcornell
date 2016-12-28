from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class Rushee(models.Model):
    id = models.AutoField(db_index=True, primary_key=True)
    first = models.CharField(db_index=True, max_length=100)
    last = models.CharField(db_index=True, max_length=100)
    netid = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    build = models.CharField(max_length=50)
    room = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    latest_signin = models.IntegerField(default=0)
    latest_signin_date = models.DateTimeField(default=timezone.now)
    
class Signin(models.Model):
    id = models.AutoField(db_index=True, primary_key=True)
    rid = models.ForeignKey(Rushee, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    qotd = models.CharField(max_length=100, default='')
    ans = models.CharField(max_length=200, default='')
    img = models.ImageField(upload_to='rush_pics/', default='/static/rush/no_img.jpeg')
    img_small = models.ImageField(upload_to='rush_pics_small/', default='/static/rush/no_img.jpeg')

class Comment(models.Model):
    id = models.AutoField(db_index=True, primary_key=True)
    rid = models.ForeignKey(Rushee, on_delete=models.CASCADE)
    broid = models.IntegerField(default=0)
    comment = models.CharField(max_length=10000)

class Event(models.Model):
    id = models.AutoField(db_index=True, primary_key=True)
    rid = models.ForeignKey(Rushee, on_delete=models.CASCADE)
    event = models.CharField(max_length=100)

class Settings(models.Model):
    name = models.CharField(db_index=True, max_length=100, primary_key=True)
    char = models.CharField(max_length=100, default='')
    val = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)

class Brothers(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(default=0)
    comments = models.BooleanField(default=True)