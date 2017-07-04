# -*- coding: utf-8 -*-
from django import forms
import models
from exileui.widgets import DatePickerWidget
from django_select2.forms import (
    HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
    ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
    Select2Widget
)
from autolavadox.service import Service
from autolavadox.forms import BaseForm


class AddVehivuloForm(forms.ModelForm):
    class Meta:
        model = models.Vehiculo
        exclude = ()
    # end class

    def __init__(self, *args, **kwargs):
        super(AddVehivuloForm, self).__init__(*args, **kwargs)
        servi = Service.get_instance()
        cuent,user,admin=servi.isUser()
        if cuent and user:
            cuenta=servi.getCuenta()
            self.fields['cliente'].queryset = models.Cliente.objects.filter(cuenta=cuenta)
            self.fields['tipo'].queryset = models.TipoVehiculo.objects.filter(estado=True,cuenta=cuenta)
        #end if
    #end def

    def save(self, commit=True):
        vehiculo = super(AddVehivuloForm, self).save(commit)
        if vehiculo.kilometraje:
            historial = models.HistorialKilometraje(vehiculo=vehiculo, kilometraje=vehiculo.kilometraje)
            historial.save()
        # end if
        return vehiculo
    # end def
# end class


class EditVehivuloForm(forms.ModelForm):
    class Meta:
        model = models.Vehiculo
        exclude = ('cliente', )
    # end class

    def __init__(self, *args, **kwargs):
        super(EditVehivuloForm, self).__init__(*args, **kwargs)
        servi = Service.get_instance()
        cuent,user,admin=servi.isUser()
        if cuent and user:
            cuenta=servi.getCuenta()
            self.fields['tipo'].queryset = models.TipoVehiculo.objects.filter(estado=True,cuenta=cuenta)
        #end if
    #end def

    def save(self, commit=True):
        vehiculo = super(EditVehivuloForm, self).save(commit)
        if vehiculo.kilometraje:
            historial = models.HistorialKilometraje(vehiculo=vehiculo, kilometraje=vehiculo.kilometraje)
            historial.save()
        # end if
        return vehiculo
    # end def
# end class


class AddClienteForm(forms.ModelForm):
    class Meta:
        model = models.Cliente
        exclude = ('dirreccion', 'correo', 'nacimiento')
    # end class

    def save(self, commit=True):
        cliente = super(AddClienteForm, self).save(commit)
        ser = Service.get_instance()
        tem_cuenta,is_user,admin = ser.isUser()
        if tem_cuenta and is_user :
            cuenta = ser.getCuenta()
            cliente.cuenta = cuenta
        elif admin:
            print 'Es un super usuario'
        #end if
        cliente.save()
        return cliente
    # end def
# end class


class AddVehivuloFormAdmin(forms.ModelForm):
    class Meta:
        model = models.Vehiculo
        exclude = ()
        widgets = {
            'tipo': Select2Widget,
            'cliente': Select2Widget
        }
    # end class

    def __init__(self, *args, **kwargs):
        super(AddVehivuloFormAdmin, self).__init__(*args, **kwargs)
        servi = Service.get_instance()
        cuent,user,admin=servi.isUser()
        if cuent and user:
            cuenta=servi.getCuenta()
            self.fields['cliente'].queryset = models.Cliente.objects.filter(cuenta=cuenta)
            self.fields['tipo'].queryset = models.TipoVehiculo.objects.filter(estado=True,cuenta=cuenta)
        #end if
    #end def

    def save(self, commit=True):
        vehiculo = super(AddVehivuloFormAdmin, self).save(commit)
        if vehiculo.kilometraje:
            historial = models.HistorialKilometraje(vehiculo=vehiculo, kilometraje=vehiculo.kilometraje)
            historial.save()
        # end if
        return vehiculo
    # end def
# end class


class AddCliente(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddCliente, self).__init__(*args, **kwargs)
        self.fields['dirreccion'].label = "Dirección "
        self.fields['nacimiento'].widget = DatePickerWidget(
            attrs={'class': 'dateclien'},
            format="%d/%m/%Y")
    # end def

    class Media:
        js = ('/static/cliente/js/clienteadd.js',)
    # end class

    class Meta:
        model = models.Cliente
        fields = ['identificacion', 'nombre', 'apellidos', 'dirreccion', 'correo',
                  'celular', 'nacimiento']
    # end class
# end class


class TipoServicioForm(BaseForm):
    class Meta:
        model = models.TipoVehiculo
        fields = ['nombre', 'descripcion']
        exclude = ['estado','cuenta']
    # end class
# end class
