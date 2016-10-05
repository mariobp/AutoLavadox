from django.contrib import admin
from exileui.admin import exileui, ExStacked, ExTabular, DateRangeEX
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

exileui.register(models.Cliente, ClienteAdmin)
exileui.register(models.TipoVehiculo)
exileui.register(models.Vehiculo)
