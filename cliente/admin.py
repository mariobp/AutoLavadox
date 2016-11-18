from django.contrib import admin
from exileui.admin import exileui, ExStacked, ExTabular, DateRangeEX
import nested_admin
import models
import forms


# Register your models here.
class VehiculoInline(admin.StackedInline):
    model = models.Vehiculo
    extra = 1
# end class


class VehiculoAdmin(admin.ModelAdmin):
    list_display = ['placa', 'tipo', 'cliente']
    list_filter = ['placa', 'tipo', 'cliente']
    form = forms.AddVehivuloFormAdmin
# end class


class ClienteAdmin(admin.ModelAdmin):
    inlines = [VehiculoInline]
    list_display = ['identificacion','nombre', 'apellidos','dirreccion','correo','celular','nacimiento']
    search_fields = ['identificacion', 'nombre', 'apellidos', 'identificacion','correo','celular']
    form = forms.AddCliente
# end class


class TipoVehiculoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    list_filter = ['nombre', 'descripcion']
    list_fileds = ['nombre', 'descripcion']
# end class
exileui.register(models.Cliente, ClienteAdmin)
exileui.register(models.TipoVehiculo, TipoVehiculoAdmin)
exileui.register(models.Vehiculo, VehiculoAdmin)
