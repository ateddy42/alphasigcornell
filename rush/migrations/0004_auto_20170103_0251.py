# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rush', '0003_auto_20170103_0235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rushee',
            name='latest_signin',
            field=models.ForeignKey(to='rush.Signin'),
        ),
    ]
