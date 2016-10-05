# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm
from django import forms
from exileui.widgets import DatePickerWidget
import models


class OperarioForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(OperarioForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar contraseña"
        self.fields['email'].label = "Correo Electrtónico"
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellidos"
        self.fields['nacimiento'].widget = DatePickerWidget(
            attrs={'class': 'date'},
            format="%m/%d/%Y")
        self.fields['telefono'].widget = forms.NumberInput()
    # end def

    class Meta:
        model = models.Empleado
        fields = ['username', 'password1', 'password2', 'email', 'first_name',
                  'last_name', 'identificacion', 'direccion', 'telefono', 'nacimiento', 'imagen']
    # end class

    def save(self, commit=True):
        operario = super(OperarioForm, self).save(commit)
        operario.is_staff = True
        operario.is_superuser = True
        operario.save()
        return operario
    # end def
# end class


class OperarioFormEdit(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OperarioFormEdit, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Correo Electrtónico"
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellidos"
        self.fields['nacimiento'].widget = DatePickerWidget(
            attrs={'class': 'date'},
            format="%m/%d/%Y")
        self.fields['telefono'].widget = forms.NumberInput()
    # end def

    class Meta:
        model = models.Empleado
        exclude = ['password1', 'password2', ]
        fields = ['username', 'email', 'first_name',
                  'last_name', 'identificacion', 'direccion', 'telefono', 'nacimiento', 'imagen']
    # end class

    def save(self, commit=True):
        operario = super(OperarioFormEdit, self).save(commit)
        operario.is_staff = True
        operario.is_superuser = True
        operario.save()
        return operario
    # end def
# end class
