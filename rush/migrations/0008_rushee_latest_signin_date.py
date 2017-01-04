# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rush', '0007_auto_20170103_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='rushee',
            name='latest_signin_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 4, 0, 27, 11, 671012, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
