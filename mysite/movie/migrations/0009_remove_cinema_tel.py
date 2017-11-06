# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0008_remove_cinema_channel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cinema',
            name='tel',
        ),
    ]
