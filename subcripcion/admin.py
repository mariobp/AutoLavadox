# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from exileui.admin import exileui, ExStacked, ExTabular, DateRangeEX
from django.contrib import admin
import models
import forms
# Register your models here.


class PlanAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'cajeros', 'operadores','recepcionistas', 'descripcion', 'valor', 'duracion'  ,'estado']
    search_fields = ['nombre', 'cajeros', 'operadores','recepcionistas', 'descripcion', 'valor', 'duracion' ,'estado']
    form = forms.PlanForm

    def get_queryset(self, request):
        queryset = super(PlanAdmin, self).get_queryset(request)
        return queryset.order_by('nombre', 'duracion','estado')
    # end def
#end class


class ClienteAdmin(admin.ModelAdmin):
    list_display = ['identificacion','first_name', 'last_name', 'direccion']
    search_fields = ['identificacion', 'firt_name', 'last_name']
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
    form = forms.SuscripcionInlineForm
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


exileui.register(models.Plan, PlanAdmin)
exileui.register(models.Suscripcion)
exileui.register(models.Cuenta, CuentaAdmin)
exileui.register(models.Cliente, ClienteAdmin)
