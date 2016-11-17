# -*- coding: utf-8 -*-
from django import forms
import models
from exileui.widgets import DatePickerWidget
from django_select2.forms import (
    HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
    ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
    Select2Widget
)


class AddVehivuloForm(forms.ModelForm):
    class Meta:
        model = models.Vehiculo
        exclude = ()
    # end class
# end class


class AddClienteForm(forms.ModelForm):
    class Meta:
        model = models.Cliente
        exclude = ('dirreccion', 'correo', 'nacimiento')
    # end class
# end class


class AddVehivuloFormAdmin(forms.ModelForm):
    class Meta:
        model = models.Vehiculo
        fields = ['placa', 'tipo', 'cliente']
        exclude = []
        widgets = {
            'tipo': Select2Widget,
            'cliente': Select2Widget
        }
    # end class
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
