# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-21 14:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('falmer_auth', '0003_auto_20170417_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='falmeruser',
            name='name',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
    ]
