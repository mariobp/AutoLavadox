#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @author: Exile
    @date: 05-07-2016
    @place: Cartagena - Colombia
    @licence: Creative Common
"""
import reports
from import_export import resources, widgets, fields
from django.db import models
from django.contrib import admin
from exileui.admin import exileui
from operacion import models as operacion
from empleados import models as empleados


class ServiciosSource(resources.ModelResource):
    orden = fields.Field(
        column_name="orden",
        attribute="orden",
        widget=widgets.ForeignKeyWidget(operacion.Orden, 'pk')
    )
    operario = fields.Field(
        column_name="Operario",
        attribute="operario",
        widget=widgets.ForeignKeyWidget(empleados.Empleado, 'operario')
    )
    tipo = fields.Field(
        column_name="Tipo",
        attribute="tipo",
        widget=widgets.ForeignKeyWidget(operacion.TipoServicio, 'tipo')
    )
    fin = fields.Field(
        column_name="fecha_nacimiento",
        attribute="fin",
        widget=widgets.DateTimeWidget(format="%Y-%m-%d %H:%M:%S")
    )
    valor = fields.Field(
        column_name="Valor",
        attribute="valor",
    )
    comision = fields.Field(
        column_name="Comisión",
        attribute="comision",

    )

    class Meta:
        model = operacion.Servicio
        fields = ['orden', 'operario', 'tipo', 'fin', 'valor', 'comision']
        export_order = ['orden', 'operario', 'tipo', 'fin', 'valor', 'comision']
    # end class
# end class

reports.register_export(operacion.Servicio, ServiciosSource)
