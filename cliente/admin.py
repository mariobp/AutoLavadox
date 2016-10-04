from django.contrib import admin
from exile_ui.admin import admin_site, ExStacked, ExTabular, DateRangeEX
import nested_admin
import models


# Register your models here.
class VehiculoInline(admin.StackedInline):
    model = models.Vehiculo
    extra = 1
# end class


class ClienteAdmin(admin.ModelAdmin):
    inlines = [VehiculoInline]
    list_display = ['nombre', 'apellidos', 'identificacion']
    list_filter = ['nombre', 'apellidos', 'identificacion']
    search_fields = ['nombre', 'apellidos', 'identificacion']
# end class

admin_site.register(models.Cliente, ClienteAdmin)
admin_site.register(models.TipoVehiculo)
admin_site.register(models.Vehiculo)
