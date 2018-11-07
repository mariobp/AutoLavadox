# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from exileui.admin import exileui, ExStacked, ExTabular, DateRangeEX
from django.contrib import admin
import models
import forms
from autolavadox import service
from autolavadox.service import Service


class PresentacionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo', 'cuenta']
    search_fields = ['nombre', 'cuenta__cliente__nombre']
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
    search_fields = ['nombre', 'descripcion', 'existencias', 'stock_minimo', 'precio_compra', 'precio_venta', 'presentacion__nombre', 'cuenta__cliente__nombre']
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
    search_fields = ['nombre', 'descripcion', 'existencias', 'stock_minimo', 'precio_compra', 'precio_venta', 'presentacion__nombre', 'cuenta__cliente__nombre']
    form = forms.ProductoVentaAdminForm

    def get_form(self, request, obj=None, *args, **kwargs):
        ser = Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if not admin:
            kwargs['form'] = forms.ProductoVentaForm
        # end if
        return super(ProductoVentaAdmin, self).get_form(request, obj, *args, **kwargs)


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
    search_fields = ['nombre', 'descripcion', 'existencias', 'stock_minimo', 'precio_compra', 'precio_venta', 'presentacion__nombre', 'cuenta__cliente__nombre']
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


class ComponenteInlineAdmin(admin.StackedInline):
    model = models.Componente
    extra = 0
    form = forms.ComponenteInlineForm
    formset = forms.ComponenteInlineFormset


class ComposicionServicioAdmin(admin.ModelAdmin):
    inlines = [ComponenteInlineAdmin]
    list_display = ['servicio', 'cuenta']
    search_fields = ['cuenta__cliente__nombre', 'servicio__nombre']
    form = forms.ComposicionServicioAdminForm

    def get_form(self, request, obj=None, *args, **kwargs):
        ser = Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if not admin:
            kwargs['form'] = forms.ComposicionServicioForm
        # end if
        return super(ComposicionServicioAdmin, self).get_form(request, obj, *args, **kwargs)

    def get_queryset(self, request):
        queryset = super(ComposicionServicioAdmin, self).get_queryset(request)
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

            return ('cuenta',)
        if admin:
            return ('servicio',)
        return ()


class ComponenteAdmin(admin.ModelAdmin):
    list_display = ['composicion', 'producto', 'cantidad', 'cuenta']
    search_fields = ['cuenta__cliente__nombre', 'producto__nombre', 'composicion__servicio__nombre']
    form = forms.ComponenteAdminForm

    def get_form(self, request, obj=None, *args, **kwargs):
        ser = Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if not admin:
            kwargs['form'] = forms.ComponenteForm
        # end if
        return super(ComponenteAdmin, self).get_form(request, obj, *args, **kwargs)

    def get_queryset(self, request):
        queryset = super(ComponenteAdmin, self).get_queryset(request)
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

            return ('cuenta',)
        if admin:
            return ('composicion', 'producto', 'cantidad', )
        return ()




# Register your models here.
exileui.register(models.Presentacion, PresentacionAdmin)
exileui.register(models.Producto, ProductoAdmin)
exileui.register(models.Venta, ProductoVentaAdmin)
exileui.register(models.Operacion, ProductoOperacionAdmin)
exileui.register(models.ComposicionServicio, ComposicionServicioAdmin)
exileui.register(models.Componente, ComponenteAdmin)