# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0010_cinema_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MovieCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=20)),
                ('channel', models.ForeignKey(to='movie.Channel')),
                ('movie', models.ForeignKey(to='movie.Movie')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='movieprice',
            name='release_time',
            field=models.CharField(default=1997, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movieprice',
            name='video_hall',
            field=models.CharField(default=4, max_length=30),
            preserve_default=False,
        ),
    ]
