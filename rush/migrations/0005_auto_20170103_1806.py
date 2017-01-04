# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rush', '0004_auto_20170103_0251'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserComment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('comments', models.BooleanField(default=True)),
                ('uid', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='brother',
            name='uid',
        ),
        migrations.DeleteModel(
            name='Brother',
        ),
    ]
