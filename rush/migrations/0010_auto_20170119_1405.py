# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rush', '0009_auto_20170103_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rushee',
            name='latest_signin_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
