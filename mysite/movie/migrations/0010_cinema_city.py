# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0009_remove_cinema_tel'),
    ]

    operations = [
        migrations.AddField(
            model_name='cinema',
            name='city',
            field=models.CharField(default='\u4e0a\u6d77', max_length=20),
            preserve_default=False,
        ),
    ]
