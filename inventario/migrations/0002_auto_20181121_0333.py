# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-21 03:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventario', '0001_initial'),
        ('subcripcion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='cuenta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='subcripcion.Cuenta'),
        ),
        migrations.AddField(
            model_name='producto',
            name='presentacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.Presentacion'),
        ),
        migrations.AddField(
            model_name='presentacion',
            name='cuenta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='subcripcion.Cuenta'),
        ),
        migrations.AddField(
            model_name='cierre',
            name='cuenta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inventario_cierre', to='subcripcion.Cuenta'),
        ),
        migrations.AlterUniqueTogether(
            name='presentacion',
            unique_together=set([('nombre', 'cuenta')]),
        ),
    ]
