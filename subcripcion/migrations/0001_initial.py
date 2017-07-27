# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-07-17 17:41
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('identificacion', models.CharField(max_length=100, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^([1-9]+[0-9]*){7,20}$'), 'Identificacion invalida', 'invalid')])),
                ('direccion', models.CharField(blank=True, max_length=200, null=True, verbose_name='Direcci\xf3n')),
                ('telefono', models.CharField(blank=True, max_length=15, null=True, verbose_name='Tel\xe9fono')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cliente_cuenta', to='subcripcion.Cliente')),
            ],
            options={
                'verbose_name': 'Cuenta',
                'verbose_name_plural': 'Cuentas',
            },
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('realizacion', models.DateTimeField(auto_now_add=True)),
                ('paga', models.BooleanField(default=False)),
                ('estado', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Factura',
                'verbose_name_plural': 'Facturas',
            },
        ),
        migrations.CreateModel(
            name='Funcionalidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, unique=True)),
                ('url', models.CharField(blank=True, max_length=300, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=800, null=True)),
                ('estado', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Funcionalidad',
                'verbose_name_plural': 'Funcionalidades',
            },
        ),
        migrations.CreateModel(
            name='InstModulo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.CharField(blank=True, max_length=800, null=True)),
                ('estado', models.BooleanField(default=True)),
                ('funcionalidades', models.ManyToManyField(to='subcripcion.Funcionalidad')),
            ],
            options={
                'verbose_name': 'Modulo plan',
                'verbose_name_plural': 'Modulos de planes',
            },
        ),
        migrations.CreateModel(
            name='Modulo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, unique=True)),
                ('descripcion', models.CharField(blank=True, max_length=800, null=True)),
                ('estado', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Modulo',
                'verbose_name_plural': 'Modulos',
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.CharField(blank=True, max_length=800, null=True)),
                ('operadores', models.IntegerField(default=0, verbose_name='N\xfamero de operadores')),
                ('cajeros', models.IntegerField(default=0, verbose_name='N\xfamero de cajeros')),
                ('recepcionistas', models.IntegerField(default=0, verbose_name='N\xfamero de recepcionistas')),
                ('operario', models.BooleanField(default=True, verbose_name='App empleados')),
                ('gerente', models.BooleanField(default=True, verbose_name='App gerente')),
                ('duracion', models.IntegerField(default=0, verbose_name='Dias de duraci\xf3n en meses')),
                ('valor', models.FloatField(default=0)),
                ('estado', models.BooleanField(default=True)),
                ('modulos', models.ManyToManyField(to='subcripcion.InstModulo')),
            ],
            options={
                'verbose_name': 'Plan',
                'verbose_name_plural': 'Planes',
            },
        ),
        migrations.CreateModel(
            name='Suscripcion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inscripcion', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Inscripci\xf3n')),
                ('inicio', models.DateTimeField(blank=True, null=True)),
                ('fin', models.DateTimeField(blank=True, null=True)),
                ('activa', models.BooleanField(default=False)),
                ('estado', models.BooleanField(default=True)),
                ('cuenta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='subcripcion.Cuenta')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subcripcion.Plan')),
            ],
            options={
                'verbose_name': 'Suscripci\xf3n',
                'verbose_name_plural': 'Subscripciones',
            },
        ),
        migrations.AddField(
            model_name='instmodulo',
            name='modulo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subcripcion.Modulo'),
        ),
        migrations.AddField(
            model_name='funcionalidad',
            name='modulo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subcripcion.Modulo'),
        ),
        migrations.AddField(
            model_name='factura',
            name='suscripcion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subcripcion.Suscripcion'),
        ),
    ]