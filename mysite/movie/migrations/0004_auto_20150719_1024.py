# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0003_cinema_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='movieprice',
            name='language_type',
            field=models.CharField(default=2, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movieprice',
            name='release_time',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movieprice',
            name='video_hall',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='movieprice',
            name='price',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
    ]
