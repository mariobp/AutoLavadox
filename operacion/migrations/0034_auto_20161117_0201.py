# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-17 07:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operacion', '0033_orden_cerrada'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orden',
            options={'verbose_name': 'Factura', 'verbose_name_plural': 'Facturas'},
        ),
    ]
