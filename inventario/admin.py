# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.html import format_html
from exileui.admin import exileui, ExStacked, ExTabular, DateRangeEX
from django.contrib import admin
import models
import forms
from autolavadox import service
from autolavadox.service import Service
from django.db import connection


class PresentacionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo', 'cuenta']
    search_fields = ['nombre']
    form = forms.PresentacionForm

    def get_form(self, request, obj=None, *args, **kwargs):
        ser = Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if admin:
            kwargs['form'] = forms.PresentacionAdminForm
        # end if
        return super(PresentacionAdmin, self).get_form(request, obj, *args, **kwargs)

    def get_queryset(self, request):
        queryset = super(PresentacionAdmin, self).get_queryset(request)
        ser = Service.get_instance()
        tem_cuenta,is_user,admin = ser.isUser()
        if tem_cuenta and is_user :
            cuenta = ser.getCuenta()
            queryset = queryset.filter(cuenta=cuenta)
        #end if
        return queryset.order_by('-id')
    # end def
# end class


class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'existencias', 'stock_minimo', 'precio_compra', 'precio_venta', 'presentacion', 'cuenta']
    search_fields = ['nombre']
    form = forms.ProductoAdminForm

    def get_form(self, request, obj=None, *args, **kwargs):
        ser = Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if not admin:
            kwargs['form'] = forms.ProductoForm
        # end if
        return super(ProductoAdmin, self).get_form(request, obj, *args, **kwargs)


    def get_queryset(self, request):
        queryset = super(ProductoAdmin, self).get_queryset(request)
        ser = Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if tem_cuenta and is_user:
            cuenta = ser.getCuenta()
            queryset = queryset.filter(cuenta=cuenta)
        # end if
        return queryset.order_by('-id')
    # end def


class ProductoVentaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'existencias', 'stock_minimo', 'precio_compra', 'precio_venta', 'presentacion', 'cuenta']
    search_fields = ['nombre', 'descripcion']
    form = forms.ProductoVentaAdminForm

    def get_form(self, request, obj=None, *args, **kwargs):
        ser = Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if not admin:
            kwargs['form'] = forms.ProductoVentaForm
        # end if
        return super(ProductoVentaAdmin, self).get_form(request, obj, *args, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        """ Set readonly attributes
         subproject is readonly when the object already exists
         fields are always readonly
        """
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if not obj and admin:
            return ('nombre', 'descripcion',  'existencias', 'stock_minimo', 'precio_compra', 'precio_venta', 'presentacion')
        if obj and admin:
            return ['cuenta']
        return ()


    def get_queryset(self, request):
        queryset = super(ProductoVentaAdmin, self).get_queryset(request)
        ser = Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if tem_cuenta and is_user:
            cuenta = ser.getCuenta()
            queryset = queryset.filter(cuenta=cuenta)
        # end if
        return queryset.order_by('-id')
    # end def


class ProductoOperacionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'existencias', 'stock_minimo', 'precio_compra', 'precio_venta', 'presentacion', 'cuenta']
    search_fields = ['nombre', 'descripcion']
    form = forms.ProductoOperacionAdminForm

    def get_form(self, request, obj=None, *args, **kwargs):
        ser = Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if not admin:
            kwargs['form'] = forms.ProductoOperacionForm
        # end if
        return super(ProductoOperacionAdmin, self).get_form(request, obj, *args, **kwargs)


    def get_queryset(self, request):
        queryset = super(ProductoOperacionAdmin, self).get_queryset(request)
        ser = Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if tem_cuenta and is_user:
            cuenta = ser.getCuenta()
            queryset = queryset.filter(cuenta=cuenta)
        # end if
        return queryset.order_by('-id')
    # end def

    def get_readonly_fields(self, request, obj=None):
        """ Set readonly attributes
         subproject is readonly when the object already exists
         fields are always readonly
        """
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if not obj and admin:
            return ('nombre', 'descripcion',  'existencias', 'stock_minimo', 'precio_compra', 'precio_venta', 'presentacion')
        if obj and admin:
            return ['cuenta']
        return ()


class CierreAdmin(admin.ModelAdmin):
    list_display = ['cuenta', 'inicio', 'fin', 'utilidad_producto_venta', 'utilidad_producto_operacion', 'imprimir_cierre']
    form = forms.CierreadminForm

    def get_queryset(self, request):
        queryset = super(CierreAdmin, self).get_queryset(request)
        ser = Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if tem_cuenta and is_user:
            cuenta = ser.getCuenta()
            queryset = queryset.filter(cuenta=cuenta)
        # end if
        return queryset.order_by('-id')
    # end def

    def get_readonly_fields(self, request, obj=None):
        """ Set readonly attributes
         subproject is readonly when the object already exists
         fields are always readonly
        """
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if obj:
            return ('cuenta', 'costo_producto_venta', 'utilidad_producto_venta', 'total_producto_venta', 'costo_producto_operacion', 'utilidad_producto_operacion', 'total_producto_operacion')
        if admin:
            return ( 'inicio', 'fin', 'costo_producto_venta', 'utilidad_producto_venta', 'total_producto_venta', 'costo_producto_operacion', 'utilidad_producto_operacion', 'total_producto_operacion', )
        return ('costo_producto_venta', 'utilidad_producto_venta', 'total_producto_venta', 'costo_producto_operacion', 'utilidad_producto_operacion', 'total_producto_operacion',)

    def get_form(self, request, obj=None, *args, **kwargs):
        ser = Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if not admin:
            kwargs['form'] = forms.CierreForm
        # end if
        return super(CierreAdmin, self).get_form(request, obj, *args, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.save()
        cursor = connection.cursor()
        sql = 'select get_cierre_inventario(%d,%d)' % (obj.id, obj.cuenta.id)
        cursor.execute(sql)
        # end if
        row = cursor.fetchone()
        resul = row[0][0]
        obj.costo_producto_venta = resul['venta_total'][0].get('compra') if resul['venta_total'] else 0
        obj.utilidad_producto_venta = resul['venta_total'][0].get('utilidad') if resul['venta_total'] else 0
        obj.total_producto_venta = resul['venta_total'][0].get('total') if resul['venta_total'] else 0
        obj.costo_producto_operacion = resul['operacion_total'][0].get('compra') if resul['operacion_total'] else 0
        obj.utilidad_producto_operacion = resul['operacion_total'][0].get('utilidad') if resul['operacion_total'] else 0
        obj.total_producto_operacion = resul['operacion_total'][0].get('total') if resul['operacion_total'] else 0
        obj.save()
    #end if

    def imprimir_cierre(self, obj):
        return format_html("<a href='/inventario/cierre/{0}/' class='imprimir'><i class='micon'>print</i>Imprimir</a>", obj.id)
    # end def

    class Media:
        js = ('/inventario/js/cierre.js')

    imprimir_cierre.allow_tags = True
    imprimir_cierre.short_description = 'Imprimir'


# Register your models here.
exileui.register(models.Presentacion, PresentacionAdmin)
#exileui.register(models.Producto, ProductoAdmin)
exileui.register(models.Venta, ProductoVentaAdmin)
exileui.register(models.Operacion, ProductoOperacionAdmin)
exileui.register(models.Cierre, CierreAdmin)
