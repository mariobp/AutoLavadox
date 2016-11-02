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
    list_display = ['orden', 'operario', 'tipo', 'inicio', 'fin', 'valor', 'comision', 'estado']
    list_filter = ['operario', 'tipo', 'estado', ('inicio', DateRangeEX)]
    search_fields = ['orden__id', ]
    list_editable = ['estado']

    def get_queryset(self, request):
        queryset = super(ServicioAdmin, self).get_queryset(request)
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
        return queryset
    # end def
# end class


class OrdenAdmin(admin.ModelAdmin):
    inlines = [ServicioInline]
    list_display = ['pk', 'fecha_orden', 'vehiculo', 'nombre_cliente','identificacion_cliente', 'valor', 'comision', 'pago', 'fin', 'imprimir_orden']
    list_filter = ['entrada', 'vehiculo', 'valor', 'comision', 'pago', ('fin', DateRangeEX)]
    list_editable = ['pago','vehiculo']
    form = forms.OrdenForm

    def save_model(self, request, obj, form, change):
        obj.save()
        total = 0
        comi = 0
        for s in models.Servicio.objects.filter(orden=obj):
            s.valor = s.tipo.costo
            s.comision = s.tipo.costo * (s.tipo.comision/100)
            comi += s.comision
            total += s.valor
            s.save()
        # end for
        obj.valor = total
        obj.comision = comi
        obj.save()
    # end if

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
        h = '0%d'%obj.entrada.hour if obj.entrada.hour <10 else '%d'%obj.entrada.hour
        m = '0%d'%obj.entrada.minute if obj.entrada.minute <10 else '%d'%obj.entrada.minute
        s = '0%d'%obj.entrada.second if obj.entrada.second <10 else '%d'%obj.entrada.second
        return '%d-%d-%d %s:%s:%s'%(obj.entrada.day,obj.entrada.month,obj.entrada.year,h,m,s)
    # end def

    def get_queryset(self, request):
        queryset = super(OrdenAdmin, self).get_queryset(request)
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
        return queryset
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
    fecha_orden.short_description = 'Realizacion'
# end class


class TipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'costo', 'comision', 'state')
    filter_horizontal = ('vehiculos',)
# end class

exileui.register(models.TipoServicio, TipoAdmin)
exileui.register(models.Servicio, ServicioAdmin)
exileui.register(models.Orden, OrdenAdmin)
