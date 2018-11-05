# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from exileui.admin import exileui, ExStacked, ExTabular, DateRangeEX
from django.contrib import admin
import models
import forms
# Register your models here.

class ModuloAdmin(admin.ModelAdmin):
    list_display = ['nombre','descripcion', 'estado']
    search_fields = ['nombre','descripcion']
    form = forms.ModuloForm

    def get_queryset(self, request):
        queryset = super(ModuloAdmin, self).get_queryset(request)
        return queryset.order_by('estado')
    # end def
#end class


class FuncionalidadAdmin(admin.ModelAdmin):
    list_display = ['modulo','nombre','descripcion','url', 'estado']
    search_fields = ['nombre','descripcion']
    form = forms.FuncionalidadForm

    def get_queryset(self, request):
        queryset = super(FuncionalidadAdmin, self).get_queryset(request)
        return queryset.order_by('modulo','nombre','estado')
    # end def
#end class


class InstModuloAdmin(admin.ModelAdmin):
    list_display = ['nombre','descripcion', 'estado']
    search_fields = ['nombre','descripcion']
    filter_horizontal = ['funcionalidades']
    form = forms.InstModuloForm

    def get_queryset(self, request):
        queryset = super(InstModuloAdmin, self).get_queryset(request)
        return queryset.order_by('modulo','nombre','estado')
    # end def
#end class


class PlanAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'cajeros', 'operadores','recepcionistas', 'descripcion', 'valor', 'duracion'  ,'estado']
    search_fields = ['nombre', 'cajeros', 'operadores','recepcionistas', 'descripcion', 'valor', 'duracion' ,'estado']
    filter_horizontal = ['modulos']
    form = forms.PlanForm

    def get_queryset(self, request):
        queryset = super(PlanAdmin, self).get_queryset(request)
        return queryset.order_by('nombre', 'duracion','estado')
    # end def
#end class


class ClienteAdmin(admin.ModelAdmin):
    list_display = ['identificacion','first_name','direccion']
    form = forms.ClienteForm

    def get_form(self, request, obj=None, *args, **kwargs):
        if obj:
            kwargs['form'] = forms.ClienteEditForm
        # end if
        return super(ClienteAdmin, self).get_form(request, obj, *args, **kwargs)
    # end def
#end class


# Register your models here.
class SuscripcionInline(admin.StackedInline):
    model = models.Suscripcion
    extra = 1

    def get_queryset(self, request):
        data = super(SuscripcionInline, self).get_queryset(request)
        return data.order_by('inscripcion')
    #end def
# end class


class CuentaAdmin(admin.ModelAdmin):
    list_display = ['cliente','estado']
    search_fields=['cliente__first_name','cliente__last_name']
    inlines = [SuscripcionInline,]
#end class


class FacturaAdmin(admin.ModelAdmin):
    list_display = ['suscripcion','cliente','paga', 'estado']
    search_fields=['suscripcion__cuenta__cliente__first_name', 'suscripcion__cuenta__cliente__last_name']
    form = forms.FacturaForm

    def cliente(self, obj):
        return '%s %s'%(obj.suscripcion.cuenta.cliente.first_name, obj.suscripcion.cuenta.cliente.last_name)
    #end def

    cliente.allow_tags = True
    cliente.short_description = 'Cliente'
#end class


#exileui.register(models.Funcionalidad)
#exileui.register(models.Modulo, ModuloAdmin)
#exileui.register(models.InstModulo, InstModuloAdmin)
exileui.register(models.Plan, PlanAdmin)
exileui.register(models.Suscripcion)
exileui.register(models.Factura, FacturaAdmin)
exileui.register(models.Cuenta, CuentaAdmin)
exileui.register(models.Cliente, ClienteAdmin)
