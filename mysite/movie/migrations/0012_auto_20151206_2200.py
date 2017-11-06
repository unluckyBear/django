# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0011_auto_20151206_2125'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moviecode',
            name='channel',
        ),
        migrations.RemoveField(
            model_name='moviecode',
            name='movie',
        ),
        migrations.DeleteModel(
            name='Movie',
        ),
        migrations.DeleteModel(
            name='MovieCode',
        ),
    ]
