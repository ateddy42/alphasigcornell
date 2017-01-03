# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Brothers',
            new_name='Brother',
        ),
        migrations.RenameModel(
            old_name='Officers',
            new_name='Officer',
        ),
    ]
