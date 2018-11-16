# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-07 02:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0010_auto_20181107_0117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componente',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.Operacion'),
        ),
        migrations.AlterField(
            model_name='composicionservicio',
            name='servicio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='operacion.TipoServicio'),
        ),
    ]