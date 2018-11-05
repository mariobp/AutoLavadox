# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-07-17 17:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('operacion', '0001_initial'),
        ('subcripcion', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='TiemposOrden',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inicio', models.DateField()),
                ('fin', models.DateField()),
                ('cuenta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tiempo_cuenta', to='subcripcion.Cuenta')),
                ('orden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='operacion.Orden')),
            ],
            options={
                'verbose_name': 'Tiempos de orden',
                'verbose_name_plural': 'Tiempos de ordenes',
            },
        ),
    ]
