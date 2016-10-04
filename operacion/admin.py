from django.contrib import admin
from exile_ui.admin import admin_site, ExStacked, ExTabular, DateRangeEX
import models
import forms
# Register your models here.


class ServicioAdmin(admin.ModelAdmin):
    list_display = ['vehiculo', 'fecha', 'tipo', 'valor', 'comision', 'pago']
    list_filter = ['vehiculo', 'fecha', 'tipo', 'valor', 'comision', 'pago']
    search_fields = ['vehiculo', 'fecha', 'tipo', 'valor', 'comision', 'pago']
    list_editable = ['pago']
    form = forms.ServicioForm

    def get_queryset(self, request):
        return models.Servicio.objects.filter(pago=False)
    # end def

# end class


admin_site.register(models.TipoServicio)
admin_site.register(models.Servicio, ServicioAdmin)
