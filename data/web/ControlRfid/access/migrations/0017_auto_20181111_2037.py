# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-11 20:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0016_auto_20181104_2118'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.RemoveField(
            model_name='telegram',
            name='user',
        ),
        migrations.DeleteModel(
            name='Telegram',
        ),
    ]
