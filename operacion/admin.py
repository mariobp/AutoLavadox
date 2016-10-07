from django.contrib import admin
from exileui.admin import exileui, ExStacked, ExTabular, DateRangeEX
import models
import forms
from daterange_filter.filter import DateRangeFilter
# Register your models here.


class ServicioInline(admin.StackedInline):
    model = models.Servicio
    form = forms.ServicioForm
    extra = 1
# end class


class ServicioAdmin(admin.ModelAdmin):
    form = forms.ServicioForm
# end class


class OrdenAdmin(admin.ModelAdmin):
    inlines = [ServicioInline]
    list_display = ['entrada', 'vehiculo', 'valor', 'comision', 'pago']
    list_editable = ['pago']
    form = forms.OrdenForm

    def save_model(self, request, obj, form, change):
        obj.save()
        total = 0
        comi = 0
        for s in models.Servicio.objects.filter(orden=obj):
            print s
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


class TipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'costo', 'comision', 'state')
    filter_horizontal = ('vehiculos',)
# end class

exileui.register(models.TipoServicio, TipoAdmin)
exileui.register(models.Servicio, ServicioAdmin)
exileui.register(models.Orden, OrdenAdmin)
