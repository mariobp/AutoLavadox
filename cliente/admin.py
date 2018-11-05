from django.contrib import admin
from exileui.admin import exileui, ExStacked, ExTabular, DateRangeEX
import nested_admin
import models
import forms
from autolavadox.views import set_queryset
from autolavadox.service import Service
from autolavadox import service
from django.db.models import Q


# Register your models here.
class VehiculoInline(admin.StackedInline):
    model = models.Vehiculo
    extra = 1
    form = forms.AddVehivuloForm
# end class


class HistorialInline(admin.StackedInline):
    model = models.HistorialKilometraje
    readonly_fields = ('kilometraje', 'fecha')
# end class


class VehiculoAdmin(admin.ModelAdmin):
    list_display = ['placa', 'tipo', 'cliente']
    list_filter = ['placa', 'tipo', 'cliente']
    form = forms.AddVehivuloFormAdmin
    inlines = [HistorialInline,]

    def get_queryset(self, request):
        queryset = super(VehiculoAdmin, self).get_queryset(request)
        ser = Service.get_instance()
        tem_cuenta,is_user,admin = ser.isUser()
        if tem_cuenta and is_user :
            cuenta = ser.getCuenta()
            queryset = queryset.filter(cliente__cuenta=cuenta)
        #end if
        return queryset.order_by('-id')
    # end def
# end class


class ClienteAdmin(admin.ModelAdmin):
    inlines = [VehiculoInline]
    list_display = ['identificacion','nombre', 'apellidos','dirreccion','correo','celular','nacimiento']
    search_fields = ['identificacion', 'nombre', 'apellidos', 'identificacion','correo','celular']
    form = forms.AddCliente

    def get_queryset(self, request):
        queryset = super(ClienteAdmin, self).get_queryset(request)
        queryset= set_queryset(queryset)
        return queryset.order_by('-id')
    # end def
# end class


class TipoVehiculoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    list_filter = ['nombre', 'descripcion']
    list_fileds = ['nombre', 'descripcion']
    form = forms.TipoServicioForm

    def get_queryset(self, request):
        queryset = super(TipoVehiculoAdmin, self).get_queryset(request)
        queryset= set_queryset(queryset)
        return queryset.filter(Q(estado=True)).order_by('-id')
    # end def
# end class
exileui.register(models.Cliente, ClienteAdmin)
exileui.register(models.TipoVehiculo, TipoVehiculoAdmin)
exileui.register(models.Vehiculo, VehiculoAdmin)
