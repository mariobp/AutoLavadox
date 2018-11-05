# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 17:45
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    dependencies = [
        ('subcripcion', '0002_auto_20170727_0931'),
        ('cliente', '0002_auto_20170727_0931'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistorialKilometraje',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kilometraje', models.CharField(max_length=100)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Historial de Kilometraje',
                'verbose_name_plural': 'Historial de Kilometraje',
            },
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='vehiculos',
        ),
        migrations.AddField(
            model_name='cliente',
            name='celular',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator(re.compile('^([1-9]+[0-9]*){6,20}$'), 'Celular no valida', 'invalid')]),
        ),
        migrations.AddField(
            model_name='cliente',
            name='correo',
            field=models.EmailField(blank=True, max_length=200, null=True, verbose_name='Correo electr\xf2nico'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='cuenta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cliente_lavado_cuenta', to='subcripcion.Cuenta'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='dirreccion',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='nacimiento',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de nacimiento'),
        ),
        migrations.AddField(
            model_name='tipovehiculo',
            name='cuenta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='subcripcion.Cuenta'),
        ),
        migrations.AddField(
            model_name='tipovehiculo',
            name='descripcion',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='cliente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cliente.Cliente'),
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='color',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='kilometraje',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='marca',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='historialkilometraje',
            name='vehiculo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cliente.Vehiculo'),
        ),
    ]
