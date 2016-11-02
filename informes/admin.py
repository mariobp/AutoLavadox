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
from cliente import models as cliente
from estadistica import models as estadistica


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
        print args, kwargs
        new = kwargs
        new['modelo'] = 1
        return super(ServiciosSource, self).export(queryset, *args, **new)
    # end def

    class Meta:
        model = operacion.Servicio
        fields = ['orden', 'nombre', 'tipo', 'fin', 'valor', 'comision']
        export_order = ['orden', 'nombre', 'tipo', 'fin', 'valor', 'comision']
    # end class
# end class


class OrdenSource(resources.ModelResource):
    fin = fields.Field(
        column_name="Fecha de realizacion",
        attribute="fin",
        widget=widgets.DateTimeWidget(format="%Y-%m-%d %H:%M:%S")
    )
    pk = fields.Field(
        column_name="Serial",
        attribute="pk",
    )
    vehiculo = fields.Field(
        column_name="Vehiculo",
        attribute="vehiculo",
        widget=widgets.ForeignKeyWidget(cliente.Vehiculo, 'placa')
    )
    valor = fields.Field(
        column_name="Valor",
        attribute="valor",
    )
    comision = fields.Field(
        column_name="Comisión",
        attribute="comision",
    )

    def export(self, queryset=None, *args, **kwargs):
        queryset = queryset
        return super(OrdenSource, self).export(queryset, *args, **kwargs)
    # end def

    class Meta:
        model = operacion.Orden
        fields = ['pk', 'fin', 'vehiculo', 'valor', 'comision']
        export_order = ['pk', 'fin', 'vehiculo', 'valor', 'comision']
    # end class
# end class


class TiemposOrdenSource(resources.ModelResource):
    serial = fields.Field(
        column_name="Serial",
        attribute="orden",
        widget=widgets.ForeignKeyWidget(operacion.Orden, 'pk')
    )
    vehiculo = fields.Field(
        column_name="vehiculo",
        attribute="orden",
        widget=widgets.ForeignKeyWidget(operacion.Orden, 'vehiculo')
    )
    inicio = fields.Field(
        column_name="Fecha de inicio",
        attribute="inicio",
        widget=widgets.DateTimeWidget(format="%Y-%m-%d %H:%M:%S")
    )
    fin = fields.Field(
        column_name="Fecha de fin",
        attribute="fin",
        widget=widgets.DateTimeWidget(format="%Y-%m-%d %H:%M:%S")
    )

    def export(self, queryset=None, *args, **kwargs):
        queryset = queryset
        return super(TiemposOrdenSource, self).export(queryset, *args, **kwargs)
    # end def

    class Meta:
        model = operacion.Orden
        fields = ['serial', 'inicio', 'fin']
        export_order = ['serial', 'inicio', 'fin']
    # end class
# end class


class OperarioSource(resources.ModelResource):
    pk = fields.Field(
        column_name="id",
        attribute="pk",
    )

    Identificacion = fields.Field(
        column_name="Identificacion",
        attribute="identificacion",
    )

    Nombre = fields.Field(
        column_name="nombre",
        attribute="first_name",
    )
    Apellidos = fields.Field(
        column_name="apellidos",
        attribute="last_name",
    )

    def export(self, queryset=None, *args, **kwargs):
        queryset = queryset
        return super(OperarioSource, self).export(queryset, *args, **kwargs)
    # end def

    class Meta:
        model = empleados.Empleado
        fields = ['pk','Identificacion', 'Nombre', 'Apellidos']
        export_order = ['pk','Identificacion', 'Nombre', 'Apellidos']
    # end class
# end class


reports.register_export(operacion.Servicio, ServiciosSource, "informes/informe.html")
reports.register_export(operacion.Orden, OrdenSource, "informes/ordenes.html")
reports.register_export(empleados.Empleado, OperarioSource, "informes/empledosproducido.html")
reports.register_export(estadistica.TiemposOrden, TiemposOrdenSource, "informes/estadisticatiemposorden.html")
