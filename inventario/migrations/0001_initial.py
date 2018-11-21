# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-21 03:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cierre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inicio', models.DateField(blank=True, null=True)),
                ('fin', models.DateField(blank=True, null=True)),
                ('costo_producto_venta', models.FloatField(default=0, verbose_name='Costo de venta')),
                ('utilidad_producto_venta', models.FloatField(default=0, verbose_name='Utilidad de venta')),
                ('total_producto_venta', models.FloatField(default=0, verbose_name='Total de venta')),
                ('costo_producto_operacion', models.FloatField(default=0, verbose_name='Costo de operacion')),
                ('utilidad_producto_operacion', models.FloatField(default=0, verbose_name='Utilidad de operacion')),
                ('total_producto_operacion', models.FloatField(default=0, verbose_name='Total de operacion')),
            ],
            options={
                'verbose_name': 'Cierre de Inventario',
                'verbose_name_plural': 'Cierres de Inventario',
            },
        ),
        migrations.CreateModel(
            name='Presentacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Presentacion',
                'verbose_name_plural': 'Presentaciones',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, null=True)),
                ('descripcion', models.TextField(blank=True, max_length=3000, null=True)),
                ('existencias', models.FloatField(default=0)),
                ('stock_minimo', models.FloatField(default=0)),
                ('precio_compra', models.FloatField(default=0)),
                ('precio_venta', models.FloatField(default=0)),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
        migrations.CreateModel(
            name='Operacion',
            fields=[
                ('producto_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='inventario.Producto')),
            ],
            options={
                'verbose_name': 'Producto de operacion',
                'verbose_name_plural': 'Productos de operacion',
            },
            bases=('inventario.producto',),
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('producto_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='inventario.Producto')),
            ],
            options={
                'verbose_name': 'Producto de venta',
                'verbose_name_plural': 'Productos de venta',
            },
            bases=('inventario.producto',),
        ),
    ]
