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
from usuarios import models as usuarios
from inventario import models as inventario
from reportes import models as reportes
from mantenimiento import models as mantenimiento
from actividades import models as actividades
from gestion_cartera import models as gestion_cartera
from django.contrib.auth.models import User
from django.db import models   
from django.contrib import admin
from exile_ui.admin import admin_site

class InsumoResource(resources.ModelResource):
    articulo = fields.Field(
        column_name='Articulo', 
        attribute='articulo', 
        widget=widgets.ForeignKeyWidget(inventario.ArticuloInsumo, 'nombre_articulo')
    )
    proveedor = fields.Field(
        column_name='Proveedor', 
        attribute='proveedor', 
        widget=widgets.ForeignKeyWidget(inventario.Proveedor, 'proveedor')
    )
    estado = fields.Field(
        column_name='Estado', 
        attribute='estado'
    )
    bodega = fields.Field(
        column_name='Bodega', 
        attribute='bodega', 
        widget=widgets.ForeignKeyWidget(inventario.Bodega, 'bodega')
    )
    cantidad_actual = fields.Field(
        column_name='Cantidad actual', 
        attribute='cantidad_actual'
    )
    en_canje_de_salida = fields.Field(
        column_name='En canje de salida', 
        attribute='en_canje_salida'
    )
    en_canje_de_entrada = fields.Field(
        column_name='En canje de entrada', 
        attribute='en_canje_entrada'
    )
    
    serial = fields.Field(
        column_name='Serial', 
        attribute='serial'
    )
    
    def get_en_canje_de_salida(self):
        salidas_bodega  = "SELECT COALESCE(0, sum(cantidad)) FROM inventario_salidadebodega WHERE insumo_id=inventario_insumo.id"
        entradas_bodega = """SELECT COALESCE(0, sum(cantidad)) 
            FROM inventario_entradadebodega as e 
            JOIN inventario_insumo as i
            ON e.insumo_destino_id=i.id
            AND i.articulo_id = inventario_insumo.articulo_id
            AND e.bodega_origen_id = inventario_insumo.bodega_id
        """
        return "(%(entradas_bodega)s - (%(salidas_bodega)s))" % {
            'entradas_bodega':entradas_bodega,
            'salidas_bodega': salidas_bodega
        }
    # end def

    def get_en_canje_de_entrada(self):
        salidas_bodega = """SELECT COALESCE(0, sum(cantidad)) 
            FROM inventario_salidadebodega as a 
            JOIN inventario_insumo as i
            ON a.insumo_id=i.id
            AND i.articulo_id = inventario_insumo.articulo_id
            AND a.bodega_destino_id = inventario_insumo.bodega_id
        """
        entradas_bodega = "SELECT COALESCE(0, sum(cantidad)) FROM inventario_entradadebodega WHERE insumo_destino_id=inventario_insumo.id"
        return "(%(entradas_bodega)s - (%(salidas_bodega)s))" % {
            'entradas_bodega':entradas_bodega,
            'salidas_bodega': salidas_bodega
        }
    # end def

    def get_cantidad_actual(self):
        entradas = "SELECT COALESCE(0, sum(cantidad)) FROM inventario_entrada WHERE insumo_id=inventario_insumo.id"
        salidas  = "SELECT COALESCE(0, sum(cantidad)) FROM inventario_salida WHERE insumo_id=inventario_insumo.id"
        
        salidas_bodega  = "SELECT COALESCE(0, sum(cantidad)) FROM inventario_salidadebodega WHERE insumo_id=inventario_insumo.id"
        entradas_bodega = "SELECT COALESCE(0, sum(cantidad)) FROM inventario_entradadebodega WHERE insumo_destino_id=inventario_insumo.id"

        return "(%(entradas)s) - (%(salidas)s) + (%(entradas_bodega)s - (%(salidas_bodega)s))" % {
            'entradas':entradas, 
            'salidas':salidas,
            'entradas_bodega':entradas_bodega,
            'salidas_bodega': salidas_bodega
        }
    # end def

    def get_estado(self):
        estado = "SELECT CASE WHEN inventario_insumo.estado THEN 'En uso' ELSE 'En desuso' END"
        return estado
    # end def

    def export(self, queryset=None, *args, **kwargs):
        queryset = queryset.extra(select={
           'cantidad_actual': self.get_cantidad_actual(),
           'en_canje_salida': self.get_en_canje_de_salida(),
           'en_canje_entrada': self.get_en_canje_de_entrada(),
           'estado': self.get_estado()
        })
        return super(InsumoResource, self).export(queryset, *args, **kwargs)
    # end def

    class Meta:
        model = inventario.Insumo
        fields = ['articulo', 'bodega', 'serial', 'proveedor', 'estado', 'cantidad_actual', 'en_canje_de_salida', 'en_canje_de_entrada']
        export_order = ['articulo', 'bodega', 'serial', 'proveedor', 'estado', 'cantidad_actual', 'en_canje_de_salida', 'en_canje_de_entrada']
    # end class
# end class

class ClienteResource(resources.ModelResource):
    nombre = fields.Field(
        column_name="nombre",
        attribute="nombre"
    )
    apellidos = fields.Field(
        column_name="apellidos",
        attribute="apellidos"
    )
    email = fields.Field(
        column_name="email",
        attribute="email"
    )
    telefono = fields.Field(
        column_name="telefono",
        attribute="telefono"
    )
    fecha_nacimiento = fields.Field(
        column_name="fecha_nacimiento",
        attribute="fecha_nacimiento",
        widget=widgets.DateTimeWidget(format="%Y-%m-%d %H:%M:%S")
    )
    nucleo_familiar = fields.Field(
        column_name="nucleo_familiar",
        attribute="nucleo_familiar"
    )
    casas = fields.Field(
        column_name="casas",
        attribute="casas"
    )
    def get_nombre(self):
        nombre = "first_name"
        return nombre
    # end def
    def get_apellidos(self):
        apellidos = "last_name"
        return apellidos
    # end def
    def get_nucleo_familiar(self):
        nucleo_familiar = "SELECT group_concat(nombre||' '||apellidos) FROM usuarios_nucleofamiliar WHERE usuario_id=usuarios_cliente.user_ptr_id"
        return nucleo_familiar
    # end def
    def get_casas(self):
        casas = "SELECT group_concat(direccion) FROM usuarios_casa WHERE cliente_id=usuarios_cliente.user_ptr_id"
        return casas
    # end def

    def export(self, queryset=None, *args, **kwargs):
        queryset = queryset.extra(select={
           'nombre': self.get_nombre(),
           'apellidos': self.get_apellidos(),
           'nucleo_familiar': self.get_nucleo_familiar(),
           'casas': self.get_casas()
        })
        return super(ClienteResource, self).export(queryset, *args, **kwargs)
    # end def
    class Meta:
        model = usuarios.Cliente
        fields = ['nombre', 'apellidos', 'email', 'telefono', 'fecha_nacimiento', 'nucleo_familiar' , 'casas']
        export_order = ['nombre', 'apellidos', 'email', 'telefono', 'fecha_nacimiento', 'nucleo_familiar' , 'casas']
    # end class
# end class

class ReporteResource(resources.ModelResource):
    nombre = fields.Field(
        column_name="Nombre",
        attribute="nombre"
    )
    tipo_de_reporte = fields.Field(
        column_name="Tipo de reporte",
        attribute="tipo_de_reporte"
    )
    descripcion = fields.Field(
        column_name="Descripción",
        attribute="descripcion"
    )
    cliente = fields.Field(
        column_name="Cliente",
        attribute="cliente"
    )
    emisor = fields.Field(
        column_name="Emisor",
        attribute="usuario",
        widget=widgets.ForeignKeyWidget(User, 'username')
    )
    fecha = fields.Field(
        column_name="fecha",
        attribute="fecha",
        widget=widgets.DateTimeWidget(format="%Y-%m-%d %H:%M:%S")
    )

    def get_cliente(self):#
        cliente = """SELECT first_name||' '||last_name
            FROM usuarios_piscina as p
            JOIN usuarios_casa as c
                ON reportes_reporte.piscina_id = p.id
                AND c.id = p.casa_id
            JOIN auth_user as u
                ON u.id = c.cliente_id

        """
        return cliente
    # end def


    def export(self, queryset=None, *args, **kwargs):
        queryset = queryset.extra(select={
           'cliente': self.get_cliente(),
        })
        return super(ReporteResource, self).export(queryset, *args, **kwargs)
    # end def
    class Meta:
        model = reportes.Reporte
        fields = ['nombre', 'tipo_de_reporte', 'descripcion', 'cliente', 'emisor', 'fecha']
        export_order = ['nombre', 'tipo_de_reporte', 'descripcion', 'cliente', 'emisor', 'fecha']
    # end class
# end class


class SolucionResource(resources.ModelResource):
    nombre = fields.Field(
        column_name="Nombre",
        attribute="nombre"
    )
    descripcion = fields.Field(
        column_name="Descripción",
        attribute="descripcion"
    )
    cliente = fields.Field(
        column_name="Cliente",
        attribute="cliente"
    )
    emisor = fields.Field(
        column_name="Emisor",
        attribute="emisor",
        widget=widgets.ForeignKeyWidget(User, 'username')
    )
    reporte = fields.Field(
        column_name="Reporte",
        attribute="reporte",
        widget=widgets.ForeignKeyWidget(reportes.Reporte, 'nombre')
    )
    fecha = fields.Field(
        column_name="fecha",
        attribute="fecha",
        widget=widgets.DateTimeWidget(format="%Y-%m-%d %H:%M:%S")
    )

    def get_cliente(self):
        cliente = """SELECT group_concat(first_name||' '||last_name)
            FROM reportes_reporte as r
            JOIN usuarios_piscina as p
                ON r.piscina_id = p.id
                AND mantenimiento_solucion.reporte_id = r.id
            JOIN usuarios_casa as c
                ON c.id = p.casa_id
            JOIN auth_user as u
                ON u.id = c.cliente_id

        """
        return cliente
    # end def


    def export(self, queryset=None, *args, **kwargs):
        queryset = queryset.extra(select={
           'cliente': self.get_cliente(),
        })
        return super(SolucionResource, self).export(queryset, *args, **kwargs)
    # end def
    class Meta:
        model = mantenimiento.Solucion
        fields = ['nombre', 'descripcion', 'cliente', 'emisor', 'reporte','fecha']
        export_order = ['nombre', 'descripcion', 'cliente', 'emisor', 'reporte','fecha']
    # end class
# end class

class ActividadResource(resources.ModelResource):
    nombre = fields.Field(
        column_name="Nombre",
        attribute="nombre",
    )
    descripcion = fields.Field(
        column_name="Descripcion",
        attribute="descripcion",
    )
    piscina = fields.Field(
        column_name="Piscina",
        attribute="piscina",
    )
    cliente = fields.Field(
        column_name="Cliente",
        attribute="piscina__cliente",
    )
    tipo_de_actividad = fields.Field(
        column_name="Tipo_de_actividad",
        attribute="tipo_de_actividad",
    )
    fecha_de_ejecucion = fields.Field(
        column_name="Fecha_de_ejecucion",
        attribute="fecha_de_ejecucion",
    )
    repetir_cada = fields.Field(
        column_name="Repetir_cada",
        attribute="repetir_cada",
    )
    unidad_de_repeticion = fields.Field(
        column_name="Unidad_de_repeticion",
        attribute="unidad_de_repeticion",
    )
    class Meta:
        model = actividades.Actividad
        fields = ['nombre', 'descripcion', 'cliente', 'piscina', 'tipo_de_actividad','fecha_de_ejecucion', 'repetir_cada', 'unidad_de_repeticion']
        export_order = ['nombre', 'descripcion', 'cliente', 'piscina', 'tipo_de_actividad','fecha_de_ejecucion', 'repetir_cada', 'unidad_de_repeticion']
    # end class
# end class

class Movimientos(models.Model):
    operacion = models.CharField(max_length=45)
    fecha = models.DateField()
    insumo = models.CharField(max_length=45)
    bodega_origen = models.CharField(max_length=45)
    bodega_destino = models.CharField(max_length=45)
    cantidad = models.IntegerField()
    usuario = models.CharField(max_length=45)

    class Meta:
        db_table = 'inventario_movimientos'
        verbose_name = "Movimientos"
        verbose_name_plural = "Movimientos"
    # end class

    def __unicode__(self, ):
        return self.insumo
    # end def
# end class

class MovimientosAdmin(admin.ModelAdmin):
    list_display = ['operacion', 'fecha', 'insumo', 'bodega_origen', 'bodega_destino', 'cantidad', 'usuario']
    list_filter  = ['operacion', 'fecha', 'insumo', 'bodega_origen', 'bodega_destino', 'cantidad', 'usuario']
    list_display_links = None

    def has_add_permission(self, request):
        return False
    # end def
    def has_delete_permission(self, request):
        return False
    # end def
# end class

class SalidaDeBodegaResource(resources.ModelResource):
    class Meta:
        model = Movimientos
        fields = ['operacion', 'fecha', 'insumo', 'bodega_origen', 'bodega_destino', 'cantidad', 'usuario']
    # end class
# end class

class InicioSeguimientoResource(resources.ModelResource):
    usuario = fields.Field(
        column_name="usuario",
        attribute="usuario__username",
    )
    class Meta:
        model = gestion_cartera.InicioSeguimiento
        fields = ['fecha', 'cliente', 'usuario', 'comentario', 'fecha_proxima', 'cerrado']
        export_order = ['fecha', 'cliente', 'usuario', 'comentario', 'fecha_proxima', 'cerrado']
    # end class
# end class

class SeguimientoResource(resources.ModelResource):
    usuario = fields.Field(
        column_name="usuario",
        attribute="usuario__username",
    )
    cliente = fields.Field(
        column_name="cliente",
        attribute="inicioseguimiento__cliente",
    )
    class Meta:
        model = gestion_cartera.InicioSeguimiento
        fields = ['fecha', 'cliente', 'usuario', 'comentario', 'fecha_proxima', 'cerrado']
        export_order = ['fecha', 'cliente', 'usuario', 'comentario', 'fecha_proxima', 'cerrado']
    # end class
# end class

reports.register_export(Movimientos, SalidaDeBodegaResource)
reports.register_export(inventario.Insumo, InsumoResource)
reports.register_export(usuarios.Cliente, ClienteResource)
reports.register_export(reportes.Reporte, ReporteResource)
reports.register_export(mantenimiento.Solucion, SolucionResource)
reports.register_export(actividades.Actividad, ActividadResource)
reports.register_export(gestion_cartera.InicioSeguimiento, InicioSeguimientoResource)
reports.register_export(gestion_cartera.Seguimiento, InicioSeguimientoResource)

admin_site.register(Movimientos, MovimientosAdmin)