from django.contrib import admin
from exileui.admin import exileui, ExStacked, ExTabular, DateRangeEX
import models
import nested_admin
import forms
from autolavadox import service
from autolavadox.views import set_queryset


class BaseAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super(BaseAdmin, self).get_queryset(request)
        return set_queryset(queryset)
    # end def
#end class


class OperarioAdmin(nested_admin.NestedModelAdmin, BaseAdmin):
    list_display = ('username', 'identificacion', 'email', 'first_name', 'last_name',
                    'direccion', 'telefono', 'nacimiento')
    list_filter =[('nacimiento', DateRangeEX)]
    search_fields = (list_display)
    form = forms.OperarioAdminForm

    def get_form(self, request, obj=None, *args, **kwargs):
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if admin and obj:
            kwargs['form'] = forms.OperarioAdminFormEdit
        if not admin and not obj:
            kwargs['form'] = forms.OperarioForm
        if obj and not admin:
            kwargs['form'] = forms.OperarioFormEdit
        # end if
        return super(OperarioAdmin, self).get_form(request, obj, *args, **kwargs)
    # end def

    class Media:
        js = ('/static/empleados/js/empleados.js',)
    # end class
# end class


class RecepcionistaAdmin(nested_admin.NestedModelAdmin, BaseAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'direccion', 'telefono', 'identificacion', 'cuenta')
    search_fields = list_display
    form = forms.RecepcionistaAdminForm

    def get_form(self, request, obj=None, *args, **kwargs):
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if admin and obj:
            kwargs['form'] = forms.RecepcionistaAdminFormEdit
        if not admin and not obj:
            kwargs['form'] = forms.RecepcionistaForm
        if obj and not admin:
            kwargs['form'] = forms.RecepcionistaFormEdit
        # end if
        return super(RecepcionistaAdmin, self).get_form(request, obj, *args, **kwargs)
    # end def
# end class


class CajeroAdmin(nested_admin.NestedModelAdmin, BaseAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'direccion', 'telefono', 'identificacion', 'cuenta')
    search_fields = list_display
    form = forms.CajeroAdminForm

    def get_form(self, request, obj=None, *args, **kwargs):
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if admin and obj:
            kwargs['form'] = forms.CajeroAdminFormEdit
        if not admin and not obj:
            kwargs['form'] = forms.CajeroForm
        if obj and not admin:
            kwargs['form'] = forms.CajeroFormEdit
        # end if
        return super(CajeroAdmin, self).get_form(request, obj, *args, **kwargs)
    # end def
# end class


class AdministradorAdmin(nested_admin.NestedModelAdmin, BaseAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'direccion', 'telefono', 'nacimiento')
    search_fields = list_display
    form = forms.AdministradorAdminForm

    def get_form(self, request, obj=None, *args, **kwargs):
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if admin and obj:
            kwargs['form'] = forms.AdministradorAdminFormEdit
        if not admin and not obj:
            kwargs['form'] = forms.AdministradorForm
        if obj and not admin:
            kwargs['form'] = forms.AdministradorFormEdit
        # end if
        return super(AdministradorAdmin, self).get_form(request, obj, *args, **kwargs)
    # end def
# end class


# Register your models here.
exileui.register(models.Empleado, OperarioAdmin)
exileui.register(models.Recepcionista, RecepcionistaAdmin)
exileui.register(models.Cajero, CajeroAdmin)
exileui.register(models.Administrador, AdministradorAdmin)
