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
    tipo = fields.Field(
        column_name="Tipo",
        attribute="tipo",
        widget=widgets.ForeignKeyWidget(operacion.TipoServicio, 'nombre')
    )
    fin = fields.Field(
        column_name="Fecha de realizacion",
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
    nombre = fields.Field(
        column_name="nombre",
        attribute="nombre"
    )

    def get_nombre(self):
        nombre = """select  case when length(__u.first_name)==0 or  __u.first_name is null  then 'operario' else __u.first_name end||' '||case when length(__u.last_name)==0 or  __u.last_name is null  then 'operario' else __u.last_name end as nombre  from auth_user as __u where "operacion_servicio"."operario_id"=__u.id"""
        return nombre
    # end def

    def export(self, queryset=None, *args, **kwargs):
        queryset = queryset.extra(select={'nombre': self.get_nombre()})
        print queryset.query
        return super(ServiciosSource, self).export(queryset, *args, **kwargs)
    # end def

    class Meta:
        model = operacion.Servicio
        fields = ['orden', 'nombre', 'tipo', 'fin', 'valor', 'comision']
        export_order = ['orden', 'nombre', 'tipo', 'fin', 'valor', 'comision']
    # end class
# end class

reports.register_export(operacion.Servicio, ServiciosSource)
