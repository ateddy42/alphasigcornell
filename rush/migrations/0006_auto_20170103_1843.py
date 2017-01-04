# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rush', '0005_auto_20170103_1806'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usercomment',
            old_name='uid',
            new_name='user',
        ),
    ]
