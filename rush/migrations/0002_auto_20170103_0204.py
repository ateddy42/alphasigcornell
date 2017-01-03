# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('rush', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Brothers',
            new_name='Brother',
        ),
        migrations.RenameModel(
            old_name='Settings',
            new_name='Setting',
        ),
        migrations.AlterField(
            model_name='rushee',
            name='latest_signin_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
