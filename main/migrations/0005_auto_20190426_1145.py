# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-04-26 15:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20181225_2138'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brother',
            options={'ordering': ['last']},
        ),
        migrations.AlterModelOptions(
            name='officer',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='officer',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
