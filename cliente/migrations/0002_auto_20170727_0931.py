# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 09:31
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    dependencies = [
        ('subcripcion', '0002_auto_20170727_0931'),
        ('cliente', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cliente',
            options={'verbose_name': 'Cliente', 'verbose_name_plural': 'Clientes'},
        ),
        migrations.AlterField(
            model_name='cliente',
            name='apellidos',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='identificacion',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(re.compile('^([1-9]+[0-9]*){7,20}$'), 'Identificacion no valida', 'invalid')]),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='nombre',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='placa',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]