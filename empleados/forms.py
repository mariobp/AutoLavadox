# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm
from django import forms
from exileui.widgets import DatePickerWidget
import models
from django.contrib.admin import widgets
from autolavadox import service
from subcripcion import models as suscripcion
from django.contrib.auth.models import Group
from django.contrib.auth.models import User


class OperarioForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(OperarioForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar contraseña"
        self.fields['email'].label = "Correo Electrtónico"
        self.fields['first_name'].label = "Nombre"
        self.fields['nacimiento'].widget = DatePickerWidget(
            attrs={'class': 'dateopera'},
            format="%d/%m/%Y")
        self.fields['telefono'].widget = forms.NumberInput()
    # end def

    class Media:
        js = ('https://storage.googleapis.com/autolavadox/static/empleados/js/dateoperario.js',)
    # end class

    class Meta:
        model = models.Empleado
        fields = ['username', 'password1', 'password2', 'email', 'first_name',
                  'last_name', 'identificacion', 'direccion', 'telefono', 'nacimiento', 'imagen']
    # end class

    def save(self, commit=True):
        operario = super(OperarioForm, self).save(commit)
        operario.is_staff = False
        operario.is_superuser = False
        ser = service.Service.get_instance()
        tem_cuenta,is_user,admin = ser.isUser()
        if tem_cuenta and is_user :
            cuenta = ser.getCuenta()
            operario.cuenta = cuenta
        elif admin:
            print 'Es un super usuario'
        #end if
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
            attrs={'class': 'dateopera'},
            format="%d/%m/%Y")
        self.fields['telefono'].widget = forms.NumberInput()
    # end def

    class Media:
        js = ('https://storage.googleapis.com/autolavadox/static/empleados/js/dateoperario.js',)
    # end class

    class Meta:
        model = models.Empleado
        exclude = ['password1', 'password2', ]
        fields = ['username', 'email', 'first_name',
                  'last_name', 'identificacion', 'direccion', 'telefono', 'nacimiento', 'imagen']
    # end class

    def save(self, commit=True):
        operario = super(OperarioFormEdit, self).save(commit)
        operario.is_staff = False
        operario.is_superuser = False
        operario.save()
        return operario
    # end def
# end class


class RecepcionistaForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RecepcionistaForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar contraseña"
        self.fields['email'].label = "Correo Electrtónico"
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellidos"
        self.fields['nacimiento'].widget = DatePickerWidget(
            attrs={'class': 'dateopera'},
            format="%d/%m/%Y")
        self.fields['telefono'].widget = forms.NumberInput()
    # end def

    class Meta:
        model = models.Recepcionista
        fields = ['username', 'password1', 'password2', 'email', 'first_name',
                  'last_name', 'identificacion', 'direccion', 'telefono', 'nacimiento', 'imagen']
    # end class

    class Media:
        js = ('https://storage.googleapis.com/autolavadox/static/empleados/js/dateoperario.js',)
    # end class

    def save(self, commit=True):
        recepcionista = super(RecepcionistaForm, self).save(commit)
        recepcionista.is_staff = True
        recepcionista.is_superuser = False
        ser = service.Service.get_instance()
        tem_cuenta,is_user,admin = ser.isUser()
        if tem_cuenta and is_user :
            cuenta = ser.getCuenta()
            recepcionista.cuenta = cuenta
        elif admin:
            print 'Es un super usuario'
        #end if
        recepcionista.save()
        return recepcionista
    # end def
# end class


class RecepcionistaFormEdit(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RecepcionistaFormEdit, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Correo Electrtónico"
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellidos"
        self.fields['nacimiento'].widget = DatePickerWidget(
            attrs={'class': 'dateopera'},
            format="%d/%m/%Y")
        self.fields['telefono'].widget = forms.NumberInput()
    # end def

    class Meta:
        model = models.Recepcionista
        exclude = ['password1', 'password2', ]
        fields = ['username', 'email', 'first_name',
                  'last_name', 'identificacion', 'direccion', 'telefono', 'nacimiento', 'imagen']
    # end class

    class Media:
        js = ('https://storage.googleapis.com/autolavadox/static/empleados/js/dateoperario.js',)
    # end class

    def save(self, commit=True):
        recepcionista = super(RecepcionistaFormEdit, self).save(commit)
        recepcionista.is_staff = True
        recepcionista.is_superuser = False
        recepcionista.save()
        return recepcionista
    # end def
# end class


class CajeroForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CajeroForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar contraseña"
        self.fields['email'].label = "Correo Electrtónico"
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellidos"
        self.fields['nacimiento'].widget = DatePickerWidget(
            attrs={'class': 'dateopera'},
            format="%d/%m/%Y")
        self.fields['telefono'].widget = forms.NumberInput()
    # end def

    class Media:
        js = ('https://storage.googleapis.com/autolavadox/static/empleados/js/dateoperario.js',)
    # end class

    class Meta:
        model = models.Cajero
        fields = ['username', 'password1', 'password2', 'email', 'first_name',
                  'last_name', 'identificacion', 'direccion', 'telefono', 'nacimiento', 'imagen']
    # end class

    def save(self, commit=True):
        cajero = super(CajeroForm, self).save(commit)
        cajero.is_staff = True
        cajero.is_superuser = False
        ser = service.Service.get_instance()
        tem_cuenta,is_user,admin = ser.isUser()
        if tem_cuenta and is_user :
            cuenta = ser.getCuenta()
            cajero.cuenta = cuenta
        elif admin:
            print 'Es un super usuario'
        #end if
        cajero.save()
        if tem_cuenta and is_user :
            usuario = User.objects.filter(id=cajero.id).first()
            grupo = Group.objects.get(name='Cajero')
            if usuario and grupo :
                usuario.groups.add(grupo)
            #end if
        #end if
        return cajero
    # end def
# end class


class CajeroFormEdit(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CajeroFormEdit, self).__init__(*args, **kwargs)
        ser = service.Service.get_instance()
        print ser.getCuenta().cliente
        self.fields['email'].label = "Correo Electrtónico"
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellidos"
        self.fields['nacimiento'].widget = DatePickerWidget(
            attrs={'class': 'dateopera'},
            format="%d/%m/%Y")
        self.fields['telefono'].widget = forms.NumberInput()
    # end def

    class Meta:
        model = models.Cajero
        exclude = ['password1', 'password2', ]
        fields = ['username', 'email', 'first_name',
                  'last_name', 'identificacion', 'direccion', 'telefono', 'nacimiento', 'imagen']
    # end class

    class Media:
        js = ('https://storage.googleapis.com/autolavadox/static/empleados/js/dateoperario.js',)
    # end class

    def save(self, commit=True):
        cajero = super(CajeroFormEdit, self).save(commit)
        cajero.is_staff = True
        cajero.is_superuser = False
        cajero.save()
        usuario = User.objects.filter(id=cajero.id).first()
        grupo = Group.objects.get(name='Cajero')
        if usuario and grupo:
            usuario.groups.add(grupo)
        #end if
        return cajero
    # end def
# end class


class AdministradorForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(AdministradorForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar contraseña"
        self.fields['email'].label = "Correo Electrtónico"
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellidos"
        self.fields['nacimiento'].widget = DatePickerWidget(
            attrs={'class': 'dateopera'},
            format="%d/%m/%Y")
        self.fields['telefono'].widget = forms.NumberInput()
    # end def

    class Media:
        js = ('https://storage.googleapis.com/autolavadox/static/empleados/js/dateoperario.js',)
    # end class

    class Meta:
        model = models.Administrador
        fields = ['username', 'password1', 'password2', 'email', 'first_name',
                  'last_name', 'identificacion', 'direccion', 'telefono', 'nacimiento', 'imagen']
    # end class

    def save(self, commit=True):
        cajero = super(AdministradorForm, self).save(commit)
        cajero.is_staff = True
        cajero.is_superuser = False
        ser = service.Service.get_instance()
        tem_cuenta,is_user,admin = ser.isUser()
        if tem_cuenta and is_user :
            cuenta = ser.getCuenta()
            cajero.cuenta = cuenta
        elif admin:
            print 'Es un super usuario'
        #end if
        cajero.save()
        if tem_cuenta and is_user :
            usuario = User.objects.filter(id=cajero.id).first()
            grupo = Group.objects.get(name='Administrador')
            if usuario and grupo :
                usuario.groups.add(grupo)
            #end if
        #end if
        return cajero
    # end def
# end class


class AdministradorFormEdit(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdministradorFormEdit, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Correo Electrtónico"
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellidos"
        self.fields['nacimiento'].widget = DatePickerWidget(
            attrs={'class': 'dateopera'},
            format="%d/%m/%Y")
        self.fields['telefono'].widget = forms.NumberInput()
    # end def

    class Meta:
        model = models.Administrador
        exclude = ['password1', 'password2', ]
        fields = ['username', 'email', 'first_name',
                  'last_name', 'identificacion', 'direccion', 'telefono', 'nacimiento', 'imagen']
    # end class

    class Media:
        js = ('https://storage.googleapis.com/autolavadox/static/empleados/js/dateoperario.js',)
    # end class

    def save(self, commit=True):
        cajero = super(AdministradorFormEdit, self).save(commit)
        cajero.is_staff = True
        cajero.is_superuser = False
        cajero.save()
        usuario = User.objects.filter(id=cajero.id).first()
        grupo = Group.objects.get(name='Administrador')
        if User.objects.filter(id=cajero.id).first() :
            usuario.groups.add(grupo)
        #end if
        return cajero
    # end def
# end class
