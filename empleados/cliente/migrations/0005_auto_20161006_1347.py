# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-06 18:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0004_tipovehiculo_descripcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiculo',
            name='cliente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cliente.Cliente'),
        ),
    ]
