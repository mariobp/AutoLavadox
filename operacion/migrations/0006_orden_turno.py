# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-05 02:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operacion', '0005_auto_20180912_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='orden',
            name='turno',
            field=models.IntegerField(default=0),
        ),
    ]