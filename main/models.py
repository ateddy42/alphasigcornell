from __future__ import unicode_literals

from django.db import models

class Officer(models.Model):
    id = models.AutoField(db_index=True, max_length=4, primary_key=True)
    position = models.TextField(max_length=100, default='')
    name = models.TextField(max_length=100, default='', null=False)
    email = models.EmailField(max_length=75, default='', null=False)
    displayed = models.BooleanField(default=True)

    def __str__(self):
        return self.position + " - " + self.name
    
class Brother(models.Model):
    id = models.AutoField(db_index=True, max_length=4, primary_key=True)
    first = models.CharField(db_index=True, max_length=100, default='')
    last = models.CharField(db_index=True, max_length=100, default='')
    major = models.TextField(max_length=100, default='')
    home = models.TextField(max_length=100, default='')
    year = models.IntegerField(default='1909')
    pic = models.ImageField(upload_to='brothers', blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.last + ", " + self.first