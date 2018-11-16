# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-12 23:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operacion', '0022_auto_20181112_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componente',
            name='producto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.Operacion'),
        ),
        migrations.AlterField(
            model_name='tiposervicio',
            name='comision',
            field=models.FloatField(default=0, verbose_name='Comisi\xf3n'),
        ),
        migrations.AlterField(
            model_name='tiposervicio',
            name='nombre',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='tiposervicio',
            name='vehiculos',
            field=models.ManyToManyField(blank=True, null=True, to='cliente.TipoVehiculo'),
        ),
    ]