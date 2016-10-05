from django.contrib import admin
from exileui.admin import admin_site, ExStacked, ExTabular, DateRangeEX
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
    list_display = ['fecha', 'vehiculo', 'valor', 'comision', 'pago']
    list_editable = ['pago']
    form = forms.OrdenForm
# end if


admin_site._registry = admin.site._registry
admin_site.register(models.TipoServicio)
admin_site.register(models.Servicio, ServicioAdmin)
admin_site.register(models.Orden, OrdenAdmin)
