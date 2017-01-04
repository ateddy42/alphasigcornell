# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rush', '0006_auto_20170103_1843'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='signin',
            options={'ordering': ('date',)},
        ),
        migrations.RemoveField(
            model_name='rushee',
            name='latest_signin',
        ),
        migrations.RemoveField(
            model_name='rushee',
            name='latest_signin_date',
        ),
    ]
