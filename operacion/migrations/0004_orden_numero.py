# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-08-24 18:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operacion', '0003_auto_20170729_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='orden',
            name='numero',
            field=models.IntegerField(default=0),
        ),
    ]