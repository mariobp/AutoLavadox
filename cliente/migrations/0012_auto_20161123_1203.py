# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-23 17:03
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0011_auto_20161120_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='identificacion',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(re.compile('^([1-9]+[0-9]*){7,20}$'), 'Identificacion no valida', 'invalid')]),
        ),
    ]