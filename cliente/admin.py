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

    def get_readonly_fields(self, request, obj=None):
        """ Set readonly attributes
         subproject is readonly when the object already exists
         fields are always readonly
        """
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if obj and admin:
            return ('cuenta',)
        if admin and not obj:
            return ('cliente','tipo', 'placa', 'marca', 'color', 'kilometraje',)
        return ()


    def get_queryset(self, request):
        queryset = super(VehiculoAdmin, self).get_queryset(request)
        ser = Service.get_instance()
        tem_cuenta,is_user,admin = ser.isUser()
        if tem_cuenta and is_user :
            cuenta = ser.getCuenta()
            #queryset = queryset.filter(cliente__cuenta=cuenta)
        #end if
        return queryset.order_by('-id')
    # end def

    def get_form(self, request, obj=None, *args, **kwargs):
        ser = Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if not admin:
            kwargs['form'] = forms.AddVehivuloFormAd
        # end if
        return super(VehiculoAdmin, self).get_form(request, obj, *args, **kwargs)
# end class


class ClienteAdmin(admin.ModelAdmin):
    inlines = [VehiculoInline]
    list_display = ['identificacion','nombre', 'apellidos','dirreccion','correo','celular','nacimiento']
    search_fields = ['identificacion', 'nombre', 'apellidos', 'identificacion','correo','celular']
    form = forms.AddClienteAdmin

    def get_queryset(self, request):
        queryset = super(ClienteAdmin, self).get_queryset(request)
        queryset= set_queryset(queryset)
        return queryset.order_by('-id')
    # end def

    def get_form(self, request, obj=None, *args, **kwargs):
        ser = Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if not admin:
            kwargs['form'] = forms.AddCliente
        # end if
        return super(ClienteAdmin, self).get_form(request, obj, *args, **kwargs)
# end class


class TipoVehiculoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'cuenta']
    list_filter = ['nombre']
    list_fileds = ['nombre', 'descripcion', 'cuenta']
    search_fields = ['nombre', 'descripcion']
    form = forms.TipoServicioFormAdmin

    def get_queryset(self, request):
        queryset = super(TipoVehiculoAdmin, self).get_queryset(request)
        queryset= set_queryset(queryset)
        return queryset.filter(Q(estado=True)).order_by('-id')
    # end def

    def get_form(self, request, obj=None, *args, **kwargs):
        ser = Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if not admin:
            kwargs['form'] = forms.TipoServicioForm
        # end if
        return super(TipoVehiculoAdmin, self).get_form(request, obj, *args, **kwargs)
# end class
exileui.register(models.Cliente, ClienteAdmin)
exileui.register(models.TipoVehiculo, TipoVehiculoAdmin)
exileui.register(models.Vehiculo, VehiculoAdmin)
