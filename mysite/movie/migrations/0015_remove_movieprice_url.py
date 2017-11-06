# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0014_movieprice_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movieprice',
            name='url',
        ),
    ]
