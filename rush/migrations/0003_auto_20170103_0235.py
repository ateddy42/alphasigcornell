# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('rush', '0002_auto_20170103_0204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brother',
            name='uid',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='broid',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
