# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20170103_0204'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='officer',
            name='year',
        ),
        migrations.AddField(
            model_name='officer',
            name='displayed',
            field=models.BooleanField(default=True),
        ),
    ]
