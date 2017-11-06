# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0013_auto_20151207_2211'),
    ]

    operations = [
        migrations.AddField(
            model_name='movieprice',
            name='url',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
