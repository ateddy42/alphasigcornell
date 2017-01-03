from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

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

    def __str__(self):
        return self.last + ", " + self.first

class Signin(models.Model):
    id = models.AutoField(db_index=True, primary_key=True)
    rid = models.ForeignKey(Rushee, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    qotd = models.CharField(max_length=100, default='')
    ans = models.CharField(max_length=200, default='')
    img = models.ImageField(upload_to='rush_pics/', default='/static/rush/no_img.jpeg')
    img_small = models.ImageField(upload_to='rush_pics_small/', default='/static/rush/no_img.jpeg')

    def __str__(self):
        return self.rid.last + ", " + self.rid.first + " - " + self.date.strftime('%Y-%m-%d - %H:%M')

class Comment(models.Model):
    id = models.AutoField(db_index=True, primary_key=True)
    rid = models.ForeignKey(Rushee, on_delete=models.CASCADE)
    broid = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=10000)

    def __str__(self):
        return self.broid.last_name + ", " + self.broid.first_name + " - " + self.rid.last + ", " + self.rid.first

class Event(models.Model):
    id = models.AutoField(db_index=True, primary_key=True)
    rid = models.ForeignKey(Rushee, on_delete=models.CASCADE)
    event = models.CharField(max_length=100)

    def __str__(self):
        return self.rid.last + ", " + self.rid.first + " - " + self.event

class Setting(models.Model):
    name = models.CharField(db_index=True, max_length=100, primary_key=True)
    char = models.CharField(max_length=100, default='')
    val = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Brother(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.BooleanField(default=True)

    def __str__(self):
        return self.uid.last_name + ", " + self.uid.first_name