# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-06 18:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operacion', '0022_remove_orden_fecha'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orden',
            old_name='entreda',
            new_name='entrada',
        ),
    ]
