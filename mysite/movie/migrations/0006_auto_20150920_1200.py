# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0005_auto_20150913_2028'),
    ]

    operations = [
        migrations.CreateModel(
            name='CinemaCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=50)),
                ('channel', models.ForeignKey(to='movie.Channel')),
                ('cinema', models.ForeignKey(to='movie.Cinema')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='movie',
            name='channel',
        ),
        migrations.DeleteModel(
            name='Movie',
        ),
        migrations.RemoveField(
            model_name='cinema',
            name='code',
        ),
        migrations.AddField(
            model_name='cinema',
            name='tel',
            field=models.CharField(default='021-xxxxxxxx', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movieprice',
            name='code',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
    ]
