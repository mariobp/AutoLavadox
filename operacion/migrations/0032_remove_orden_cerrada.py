# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-17 05:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operacion', '0031_auto_20161117_0010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orden',
            name='cerrada',
        ),
    ]
