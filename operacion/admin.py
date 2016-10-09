from django.contrib import admin
from exileui.admin import exileui, ExStacked, ExTabular, DateRangeEX
import models
import forms
from datetime import datetime
from daterange_filter.filter import DateRangeFilter
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
    list_display = ['pk', 'entrada', 'vehiculo', 'valor', 'comision', 'pago', 'fin']
    list_filter = ['entrada', 'vehiculo', 'valor', 'comision', 'pago', ('fin', DateRangeEX)]
    list_editable = ['pago']
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
# end class


class TipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'costo', 'comision', 'state')
    filter_horizontal = ('vehiculos',)
# end class

exileui.register(models.TipoServicio, TipoAdmin)
exileui.register(models.Servicio, ServicioAdmin)
exileui.register(models.Orden, OrdenAdmin)
