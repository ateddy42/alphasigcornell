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
    latest_signin_date = models.DateTimeField(null=True, blank=True)

    def latest_signin(self):
        return self.signin_set.all().order_by('-date')[0]

    def __str__(self):
        return self.last + ", " + self.first

class Signin(models.Model):
    id = models.AutoField(db_index=True, primary_key=True)
    rush = models.ForeignKey(Rushee, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    qotd = models.CharField(max_length=100, default='')
    ans = models.CharField(max_length=200, default='')
    img = models.ImageField(upload_to='rush_pics/', default='/static/rush/no_img.jpeg')
    img_small = models.ImageField(upload_to='rush_pics_small/', default='/static/rush/no_img.jpeg')

    def __str__(self):
        return self.rush.last + ", " + self.rush.first + " - " + self.date.strftime('%Y-%m-%d - %H:%M')

    class Meta:
        ordering = ('date',)

class Comment(models.Model):
    id = models.AutoField(db_index=True, primary_key=True)
    rush = models.ForeignKey(Rushee, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=10000)

    def __str__(self):
        return self.user.last_name + ", " + self.user.first_name + " - " + self.rush.last + ", " + self.rush.first

class Event(models.Model):
    id = models.AutoField(db_index=True, primary_key=True)
    rush = models.ForeignKey(Rushee, on_delete=models.CASCADE)
    event = models.CharField(max_length=100)

    def __str__(self):
        return self.rush.last + ", " + self.rush.first + " - " + self.event

class Setting(models.Model):
    name = models.CharField(db_index=True, max_length=100, primary_key=True)
    char = models.CharField(max_length=100, default='')
    val = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class UserComment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User)
    comments = models.BooleanField(default=True)

    def __str__(self):
        return self.user.last_name + ", " + self.user.first_name