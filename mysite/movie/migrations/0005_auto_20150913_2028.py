# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0004_auto_20150719_1024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movieprice',
            name='release_time',
        ),
        migrations.RemoveField(
            model_name='movieprice',
            name='video_hall',
        ),
    ]
