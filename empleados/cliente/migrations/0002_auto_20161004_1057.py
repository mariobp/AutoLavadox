# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-04 15:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cliente',
            options={'verbose_name': 'Cliente', 'verbose_name_plural': 'Clientes'},
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='vehiculos',
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='cliente',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cliente.Cliente'),
            preserve_default=False,
        ),
    ]
