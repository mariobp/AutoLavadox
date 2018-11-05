# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-04 13:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificacion', models.CharField(max_length=20, unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=300)),
            ],
            options={
                'verbose_name': 'Trabajador',
                'verbose_name_plural': 'Trabajadores',
            },
        ),
        migrations.CreateModel(
            name='TipoVehiculo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, unique=True)),
                ('estado', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Tipo de Vehiculo',
                'verbose_name_plural': 'Tipos de vehiculo',
            },
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placa', models.CharField(max_length=10, unique=True)),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cliente.TipoVehiculo')),
            ],
            options={
                'verbose_name': 'Vehiculo',
                'verbose_name_plural': 'Vehiculos',
            },
        ),
        migrations.AddField(
            model_name='cliente',
            name='vehiculos',
            field=models.ManyToManyField(blank=True, null=True, to='cliente.Vehiculo'),
        ),
    ]
