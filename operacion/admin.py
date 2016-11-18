# -*- coding: utf-8 -*-
from django.contrib import admin
from exileui.admin import exileui, ExStacked, ExTabular, DateRangeEX
import models
import forms
from datetime import datetime
from daterange_filter.filter import DateRangeFilter
from django.utils.html import format_html
# Register your models here.


class ServicioInline(admin.StackedInline):
    model = models.Servicio
    form = forms.ServicioForm
    extra = 1
# end class


class ServicioAdmin(admin.ModelAdmin):
    form = forms.ServicioForm
    list_display = ['orden','placa_nombre',  'tipo', 'inicio', 'fin', 'valor', 'comision', 'estado']
    list_filter = [('inicio', DateRangeEX)]
    search_fields = ['orden__id', ]
    list_editable = ['estado']

    def placa_nombre(self, obj):
        if obj.orden.vehiculo.placa :
            return obj.orden.vehiculo.placa
        # end if
        return '-----'
    #

    def get_queryset(self, request):
        queryset = super(ServicioAdmin, self).get_queryset(request)
        """
        drf__inicio__gte = request.GET.get('drf__inicio__gte', False)
        drf__inicio__lte = request.GET.get('drf__inicio__lte', False)
        now = datetime.now()
        if not drf__inicio__gte and not drf__inicio__lte:
            return queryset.filter(
                inicio__year = now.year,
                inicio__month = now.month,
                inicio__day = now.day,
            )
        # end if
        """
        return queryset.filter(status=True).order_by('-id')
    # end def

    class Media:
        js = ('/static/operacion/js/servicio.js',)
    # end class

    placa_nombre.allow_tags = True
    placa_nombre.short_description = 'Placa'
# end class


class OrdenAdmin(admin.ModelAdmin):
    inlines = [ServicioInline]
    list_display = ['id_reporte', 'fecha_orden', 'fecha_orden_fin', 'vehiculo', 'nombre_cliente','identificacion_cliente', 'valor', 'comision','cerrada', 'pago', 'imprimir_orden']
    list_filter = [('fin', DateRangeEX)]
    search_fields = ['entrada', 'vehiculo', 'valor', 'comision', 'pago']
    list_editable = ['cerrada', 'pago','vehiculo']
    form = forms.OrdenForm
    list_display_links = ['id_reporte']

    def save_model(self, request, obj, form, change):
        obj.save()
        total = 0
        comi = 0
        for s in models.Servicio.objects.filter(orden=obj):
            if s.status and s.estado :
                s.valor = s.tipo.costo
                s.comision = s.tipo.comision
                comi += s.comision
                total += s.valor
                s.save()
            # end if
        # end for
        obj.valor = total
        obj.comision = comi
        obj.save()
    # end if

    def id_reporte(self, obj):
        i = 0
        men = ''
        while i < 10 - len(str(obj.pk)):
            men = men + '0'
            i = i+1
        # end ford
        return '%s%d' % (men, obj.pk)
    # end def

    def imprimir_orden(self, obj):
        return format_html("<a href='{0}' class='imprimir'><i class='micon'>print</i>Imprimir</a>", obj.id)
    # end def

    def nombre_cliente(self, obj):
        return '%s %s'%(obj.vehiculo.cliente.nombre,obj.vehiculo.cliente.apellidos) if obj.vehiculo.cliente else '---- -----'
    #end

    def identificacion_cliente(self, obj):
        return '%s'%(obj.vehiculo.cliente.identificacion) if obj.vehiculo.cliente else '-------'
    #end

    def fecha_orden(self, obj):
        if obj.entrada:
            h = '0%d'%obj.entrada.hour if obj.entrada.hour <10 else '%d'%obj.entrada.hour
            m = '0%d'%obj.entrada.minute if obj.entrada.minute <10 else '%d'%obj.entrada.minute
            s = '0%d'%obj.entrada.second if obj.entrada.second <10 else '%d'%obj.entrada.second
            return '%d-%d-%d %s:%s:%s'%(obj.entrada.day,obj.entrada.month,obj.entrada.year,h,m,s)
        else:
            return '--/--/--'
    # end def

    def fecha_orden_fin(self, obj):
        if obj.fin :
            h = '0%d'%obj.fin.hour if obj.fin.hour <10 else '%d'%obj.fin.hour
            m = '0%d'%obj.fin.minute if obj.fin.minute <10 else '%d'%obj.fin.minute
            s = '0%d'%obj.fin.second if obj.fin.second <10 else '%d'%obj.fin.second
            return '%d-%d-%d %s:%s:%s'%(obj.fin.day,obj.fin.month,obj.fin.year,h,m,s)
        else:
            return '--/--/--'
    # end def

    def get_queryset(self, request):
        queryset = super(OrdenAdmin, self).get_queryset(request)
        """
        drf__inicio__gte = request.GET.get('drf__entrada__gte', False)
        drf__inicio__lte = request.GET.get('drf__entrada__lte', False)
        now = datetime.now()
        if not drf__inicio__gte and not drf__inicio__lte:
            return queryset.filter(
                entrada__year = now.year,
                entrada__month = now.month,
                entrada__day = now.day,
            )
        # end if
        """

        return queryset.order_by('-id')
    # end def

    class Media:
        js = ('/static/operacion/js/operacion.js',)
        css = {
            'all': ('/static/operacion/css/operacion.css',)
        }
    # end class

    imprimir_orden.allow_tags = True
    imprimir_orden.short_description = 'Imprimir Orden'
    nombre_cliente.allow_tags = True
    nombre_cliente.short_description = 'Propietario'
    identificacion_cliente.allow_tags = True
    identificacion_cliente.short_description = 'Identificacion'
    fecha_orden.allow_tags = True
    fecha_orden.short_description = 'Realización'
    fecha_orden_fin.allow_tags = True
    fecha_orden_fin.short_description = 'Finalización'
    id_reporte.allow_tags = True
    id_reporte.short_description = 'Factura'
# end class


class TipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'costo', 'comision', 'state')
    filter_horizontal = ('vehiculos',)
# end class

exileui.register(models.TipoServicio, TipoAdmin)
exileui.register(models.Servicio, ServicioAdmin)
exileui.register(models.Orden, OrdenAdmin)
