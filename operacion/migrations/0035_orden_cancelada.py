# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-20 16:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operacion', '0034_auto_20161117_0201'),
    ]

    operations = [
        migrations.AddField(
            model_name='orden',
            name='cancelada',
            field=models.BooleanField(default=False),
        ),
    ]
