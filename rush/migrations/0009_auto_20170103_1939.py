# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rush', '0008_rushee_latest_signin_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='rid',
            new_name='rush',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='broid',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='rid',
            new_name='rush',
        ),
        migrations.RenameField(
            model_name='signin',
            old_name='rid',
            new_name='rush',
        ),
    ]
