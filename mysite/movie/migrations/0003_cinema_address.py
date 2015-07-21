# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_channel_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='cinema',
            name='address',
            field=models.CharField(default=datetime.datetime(2015, 7, 18, 13, 22, 12, 910000, tzinfo=utc), max_length=800),
            preserve_default=False,
        ),
    ]
