# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-26 02:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20170103_0219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brother',
            name='pic',
            field=models.ImageField(blank=True, null=True, upload_to='brothers'),
        ),
    ]
