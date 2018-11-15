# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db.models import Q
from exileui.widgets import DatePickerWidget
import models
from django.contrib.admin import widgets
from autolavadox import service
from autolavadox.settings import SERVER_STATIC
from subcripcion import models as suscripcion
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from easy_select2 import apply_select2, Select2Multiple
from django.contrib.admin import widgets


class OperarioForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(OperarioForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar contraseña"
        self.fields['email'].label = "Correo Electrtónico"
        self.fields['first_name'].label = "Nombre"
        self.fields['nacimiento'].widget = widgets.AdminDateWidget()
        self.fields['telefono'].widget = forms.NumberInput()
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if tem_cuenta and is_user:
            self.cuenta = ser.getCuenta()
    # end def

    def clean(self):
        data = super(OperarioForm, self).clean()
        if self.fields.has_key('identificacion'):
            if data.get('identificacion') and self.cuenta:
                cajero = models.Empleado.objects.filter(Q(cuenta=self.cuenta, identificacion=data.get('identificacion'))&~Q(id=self.instance.id if self.instance else 0))
                if cajero:
                    self.add_error('identificacion', 'El numero de identificacion se encuentra registrado.')
            elif not data.get('identificacion'):
                self.add_error('identificacion', 'Debe registrar un numero de identificacion.')

    class Media:
        js = ('{}/static/empleados/js/dateoperario.js'.format(SERVER_STATIC),)
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


class OperarioAdminForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(OperarioAdminForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar contraseña"
        self.fields['email'].label = "Correo Electrtónico"
        self.fields['first_name'].label = "Nombre"
        self.fields['nacimiento'].widget = widgets.AdminDateWidget()
        self.fields['telefono'].widget = forms.NumberInput()
    # end def

    class Media:
        js = ('{}/static/empleados/js/dateoperario.js'.format(SERVER_STATIC),)
    # end class

    def clean(self):
        data = super(OperarioAdminForm, self).clean()
        if self.fields.has_key('cuenta'):
            if not data.get('cuenta'):
                self.add_error('cuenta', 'Debe seleccionar una cuenta.')
        if self.fields.has_key('identificacion'):
            if data.get('identificacion') and data.get('cuenta'):
                cajero = models.Empleado.objects.filter(Q(cuenta=data.get('cuenta'), identificacion=data.get('identificacion'))&~Q(id=self.instance.id if self.instance else 0))
                if cajero:
                    self.add_error('identificacion', 'El numero de identificacion se encuentra registrado.')
            elif not data.get('identificacion'):
                self.add_error('identificacion', 'Debe registrar un numero de identificacion.')

    class Meta:
        model = models.Empleado
        fields = ['cuenta', 'username', 'password1', 'password2', 'email', 'first_name',
                  'last_name', 'identificacion', 'direccion', 'telefono', 'nacimiento', 'imagen']
        widgets = {
            'cuenta': apply_select2(forms.Select),
        }
    # end class

    def save(self, commit=True):
        operario = super(OperarioAdminForm, self).save(commit)
        operario.is_staff = False
        operario.is_superuser = False
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
        self.fields['nacimiento'].widget = widgets.AdminDateWidget()
        self.fields['telefono'].widget = forms.NumberInput()
    # end def

    class Media:
        js = ('{}/static/empleados/js/dateoperario.js'.format(SERVER_STATIC),)
    # end class

    def clean(self):
        data = super(OperarioFormEdit, self).clean()
        if self.fields.has_key('identificacion'):
            if data.get('identificacion') and self.cuenta:
                cajero = models.Empleado.objects.filter(Q(cuenta=self.cuenta, identificacion=data.get('identificacion'))&~Q(id=self.instance.id if self.instance else 0))
                if cajero:
                    self.add_error('identificacion', 'El numero de identificacion se encuentra registrado.')
            elif not data.get('identificacion'):
                self.add_error('identificacion', 'Debe registrar un numero de identificacion.')

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


class OperarioAdminFormEdit(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OperarioAdminFormEdit, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Correo Electrtónico"
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellidos"
        self.fields['nacimiento'].widget = widgets.AdminDateWidget()
        self.fields['telefono'].widget = forms.NumberInput()
    # end def

    class Media:
        js = ('{}/static/empleados/js/dateoperario.js'.format(SERVER_STATIC),)
    # end class

    class Meta:
        model = models.Empleado
        exclude = ['password1', 'password2', ]
        fields = ['cuenta', 'username', 'email', 'first_name',
                  'last_name', 'identificacion', 'direccion', 'telefono', 'nacimiento', 'imagen']
        widgets = {
            'cuenta': apply_select2(forms.Select),
        }
    # end class

    def clean(self):
        data = super(OperarioAdminFormEdit, self).clean()
        if self.fields.has_key('cuenta'):
            if not data.get('cuenta'):
                self.add_error('cuenta', 'Debe seleccionar una cuenta.')
        if self.fields.has_key('identificacion'):
            if data.get('identificacion') and data.get('cuenta'):
                cajero = models.Empleado.objects.filter(Q(cuenta=data.get('cuenta'), identificacion=data.get('identificacion'))&~Q(id=self.instance.id if self.instance else 0))
                if cajero:
                    self.add_error('identificacion', 'El numero de identificacion se encuentra registrado.')
            elif not data.get('identificacion'):
                self.add_error('identificacion', 'Debe registrar un numero de identificacion.')

    def save(self, commit=True):
        operario = super(OperarioAdminFormEdit, self).save(commit)
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
        self.fields['nacimiento'].widget = widgets.AdminDateWidget()
        self.fields['telefono'].widget = forms.NumberInput()
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if tem_cuenta and is_user:
            self.cuenta = ser.getCuenta()
    # end def

    class Meta:
        model = models.Recepcionista
        fields = ['username', 'password1', 'password2', 'email', 'first_name',
                  'last_name', 'identificacion', 'direccion', 'telefono', 'nacimiento', 'imagen']
    # end class

    class Media:
        js = ('{}/static/empleados/js/dateoperario.js'.format(SERVER_STATIC),)
    # end class

    def clean(self):
        data = super(RecepcionistaForm, self).clean()
        if self.fields.has_key('identificacion'):
            if data.get('identificacion') and self.cuenta:
                cajero = models.Recepcionista.objects.filter(Q(cuenta=self.cuenta, identificacion=data.get('identificacion'))&~Q(id=self.instance.id if self.instance else 0))
                if cajero:
                    self.add_error('identificacion', 'El numero de identificacion se encuentra registrado.')
            elif not data.get('identificacion'):
                self.add_error('identificacion', 'Debe registrar un numero de identificacion.')

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


class RecepcionistaAdminForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RecepcionistaAdminForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar contraseña"
        self.fields['email'].label = "Correo Electrtónico"
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellidos"
        self.fields['nacimiento'].widget = widgets.AdminDateWidget()
        self.fields['telefono'].widget = forms.NumberInput()
    # end def

    class Meta:
        model = models.Recepcionista
        fields = ['cuenta', 'username', 'password1', 'password2', 'email', 'first_name',
                  'last_name', 'identificacion', 'direccion', 'telefono', 'nacimiento', 'imagen']
        widgets = {
            'cuenta': apply_select2(forms.Select),
        }
    # end class

    class Media:
        js = ('{}/static/empleados/js/dateoperario.js'.format(SERVER_STATIC),)
    # end class

    def clean(self):
        data = super(RecepcionistaAdminForm, self).clean()
        if self.fields.has_key('cuenta'):
            if not data.get('cuenta'):
                self.add_error('cuenta', 'Debe seleccionar una cuenta.')
        if self.fields.has_key('identificacion'):
            if data.get('identificacion') and data.get('cuenta'):
                cajero = models.Recepcionista.objects.filter(Q(cuenta=data.get('cuenta'), identificacion=data.get('identificacion'))&~Q(id=self.instance.id if self.instance else 0))
                if cajero:
                    self.add_error('identificacion', 'El numero de identificacion se encuentra registrado.')
            elif not data.get('identificacion'):
                self.add_error('identificacion', 'Debe registrar un numero de identificacion.')

    def save(self, commit=True):
        recepcionista = super(RecepcionistaAdminForm, self).save(commit)
        recepcionista.is_staff = True
        recepcionista.is_superuser = False
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
        self.fields['nacimiento'].widget = widgets.AdminDateWidget()
        self.fields['telefono'].widget = forms.NumberInput()
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if tem_cuenta and is_user:
            self.cuenta = ser.getCuenta()
    # end def

    class Meta:
        model = models.Recepcionista
        exclude = ['password1', 'password2', ]
        fields = ['username', 'email', 'first_name',
                  'last_name', 'identificacion', 'direccion', 'telefono', 'nacimiento', 'imagen']
    # end class

    class Media:
        js = ('{}/static/empleados/js/dateoperario.js'.format(SERVER_STATIC),)
    # end class

    def clean(self):
        data = super(RecepcionistaFormEdit, self).clean()
        if self.fields.has_key('identificacion'):
            if data.get('identificacion') and self.cuenta:
                cajero = models.Recepcionista.objects.filter(Q(cuenta=self.cuenta, identificacion=data.get('identificacion'))&~Q(id=self.instance.id if self.instance else 0))
                if cajero:
                    self.add_error('identificacion', 'El numero de identificacion se encuentra registrado.')
            elif not data.get('identificacion'):
                self.add_error('identificacion', 'Debe registrar un numero de identificacion.')

    def save(self, commit=True):
        recepcionista = super(RecepcionistaFormEdit, self).save(commit)
        recepcionista.is_staff = True
        recepcionista.is_superuser = False
        recepcionista.save()
        return recepcionista
    # end def
# end class


class RecepcionistaAdminFormEdit(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RecepcionistaAdminFormEdit, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Correo Electrtónico"
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellidos"
        self.fields['nacimiento'].widget = widgets.AdminDateWidget()
        self.fields['telefono'].widget = forms.NumberInput()
    # end def

    class Meta:
        model = models.Recepcionista
        exclude = ['password1', 'password2', ]
        fields = ['cuenta', 'username', 'email', 'first_name',
                  'last_name', 'identificacion', 'direccion', 'telefono', 'nacimiento', 'imagen']
        widgets = {
            'cuenta': apply_select2(forms.Select),
        }
    # end class

    def clean(self):
        data = super(RecepcionistaAdminFormEdit, self).clean()
        if self.fields.has_key('cuenta'):
            if not data.get('cuenta'):
                self.add_error('cuenta', 'Debe seleccionar una cuenta.')
        if self.fields.has_key('identificacion'):
            if data.get('identificacion') and data.get('cuenta'):
                cajero = models.Recepcionista.objects.filter(Q(cuenta=data.get('cuenta'), identificacion=data.get('identificacion'))&~Q(id=self.instance.id if self.instance else 0))
                if cajero:
                    self.add_error('identificacion', 'El numero de identificacion se encuentra registrado.')
            elif not data.get('identificacion'):
                self.add_error('identificacion', 'Debe registrar un numero de identificacion.')


    class Media:
        js = ('{}/static/empleados/js/dateoperario.js'.format(SERVER_STATIC),)
    # end class

    def save(self, commit=True):
        recepcionista = super(RecepcionistaAdminFormEdit, self).save(commit)
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
        self.fields['nacimiento'].widget = widgets.AdminDateWidget()
        self.fields['telefono'].widget = forms.NumberInput()
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        self.cuenta = None
        if tem_cuenta and is_user:
            self.cuenta = ser.getCuenta()
    # end def

    class Media:
        js = ('{}/static/empleados/js/dateoperario.js'.format(SERVER_STATIC),)
    # end class

    class Meta:
        model = models.Cajero
        fields = ['username', 'password1', 'password2', 'email', 'first_name',
                  'last_name', 'identificacion', 'direccion', 'telefono', 'nacimiento', 'imagen']
    # end class

    def clean(self):
        data = super(CajeroForm, self).clean()
        if data.get('identificacion') and self.cuenta:
            cajero = models.Cajero.objects.filter(Q(cuenta=self.instance.cuenta, identificacion=data.get('identificacion'))&~Q(id=self.instance.id if self.instance else 0))
            if cajero:
                self.add_error('identificacion', 'El numero de identificacion se encuentra registrado.')
        elif not data.get('identificacion') :
            self.add_error('identificacion', 'Debe registrar un numero de identificacion.')

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


class CajeroAdminForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CajeroAdminForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar contraseña"
        self.fields['email'].label = "Correo Electrtónico"
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellidos"
        self.fields['nacimiento'].widget = widgets.AdminDateWidget()
        self.fields['telefono'].widget = forms.NumberInput()
    # end def

    class Media:
        js = ('{}/static/empleados/js/dateoperario.js'.format(SERVER_STATIC),)
    # end class

    class Meta:
        model = models.Cajero
        fields = ['cuenta', 'username', 'password1', 'password2', 'email', 'first_name',
                  'last_name', 'identificacion', 'direccion', 'telefono', 'nacimiento', 'imagen']
        widgets = {
            'cuenta': apply_select2(forms.Select),
        }
    # end class

    def clean(self):
        data = super(CajeroAdminForm, self).clean()
        if self.fields.has_key('cuenta'):
            if not data.get('cuenta'):
                self.add_error('cuenta', 'Debe seleccionar una cuenta.')
        if self.fields.has_key('identificacion'):
            if data.get('identificacion') and data.get('cuenta'):
                cajero = models.Cajero.objects.filter(Q(cuenta=data.get('cuenta'), identificacion=data.get('identificacion'))&~Q(id=self.instance.id if self.instance else 0))
                if cajero:
                    self.add_error('identificacion', 'El numero de identificacion se encuentra registrado.')
            elif not data.get('identificacion'):
                self.add_error('identificacion', 'Debe registrar un numero de identificacion.')

    def save(self, commit=True):
        cajero = super(CajeroAdminForm, self).save(commit)
        cajero.is_staff = True
        cajero.is_superuser = False
        cajero.save()
        usuario = User.objects.filter(id=cajero.id).first()
        grupo = Group.objects.get(name='Cajero')
        if usuario and grupo :
            usuario.groups.add(grupo)
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
        self.fields['nacimiento'].widget = widgets.AdminDateWidget()
        self.fields['telefono'].widget = forms.NumberInput()
    # end def

    class Meta:
        model = models.Cajero
        exclude = ['password1', 'password2', ]
        fields = ['username', 'email', 'first_name',
                  'last_name', 'identificacion', 'direccion', 'telefono', 'nacimiento', 'imagen']
    # end class

    class Media:
        js = ('{}/static/empleados/js/dateoperario.js'.format(SERVER_STATIC),)
    # end class

    def clean(self):
        data = super(CajeroFormEdit, self).clean()
        if self.fields.has_key('identificacion'):
            if data.get('identificacion'):
                cajero = models.Cajero.objects.filter(Q(cuenta=self.instance.cuenta, identificacion=data.get('identificacion'))&~Q(id=self.instance.id if self.instance else 0))
                if cajero:
                    self.add_error('identificacion', 'El numero de identificacion se encuentra registrado.')
            elif not data.get('identificacion'):
                self.add_error('identificacion', 'Debe registrar un numero de identificacion.')

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


class CajeroAdminFormEdit(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CajeroAdminFormEdit, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Correo Electrtónico"
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellidos"
        self.fields['nacimiento'].widget = widgets.AdminDateWidget()
        self.fields['telefono'].widget = forms.NumberInput()
    # end def

    class Meta:
        model = models.Cajero
        exclude = ['password1', 'password2', ]
        fields = ['cuenta', 'username', 'email', 'first_name',
                  'last_name', 'identificacion', 'direccion', 'telefono', 'nacimiento', 'imagen']

        widgets = {
            'cuenta': apply_select2(forms.Select),
        }
    # end class

    class Media:
        js = ('{}/static/empleados/js/dateoperario.js'.format(SERVER_STATIC),)
    # end class

    def clean(self):
        data = super(CajeroAdminFormEdit, self).clean()
        if self.fields.has_key('cuenta'):
            if not data.get('cuenta'):
                self.add_error('cuenta', 'Debe seleccionar una cuenta.')
        if self.fields.has_key('identificacion'):
            if data.get('identificacion') and data.get('cuenta'):
                cajero = models.Cajero.objects.filter(Q(cuenta=data.get('cuenta'), identificacion=data.get('identificacion'))&~Q(id=self.instance.id if self.instance else 0))
                if cajero:
                    self.add_error('identificacion', 'El numero de identificacion se encuentra registrado.')
            elif not data.get('identificacion'):
                self.add_error('identificacion', 'Debe registrar un numero de identificacion.')

    def save(self, commit=True):
        cajero = super(CajeroAdminFormEdit, self).save(commit)
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
        self.fields['nacimiento'].widget = widgets.AdminDateWidget()
        self.fields['telefono'].widget = forms.NumberInput()
    # end def

    class Media:
        js = ('{}/static/empleados/js/dateoperario.js'.format(SERVER_STATIC),)
    # end class

    class Meta:
        model = models.Administrador
        fields = ['username', 'password1', 'password2', 'email', 'first_name',
                  'last_name', 'identificacion', 'direccion', 'telefono', 'nacimiento', 'imagen']
    # end class

    def clean(self):
        data = super(AdministradorAdminForm, self).clean()
        if not data.get('identificacion'):
            self.add_error('identificacion', 'Debe digitar el numero de identificacion.')

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


class AdministradorAdminForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(AdministradorAdminForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar contraseña"
        self.fields['email'].label = "Correo Electrtónico"
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellidos"
        self.fields['nacimiento'].widget = widgets.AdminDateWidget()
        self.fields['telefono'].widget = forms.NumberInput()
    # end def

    class Media:
        js = ('{}/static/empleados/js/dateoperario.js'.format(SERVER_STATIC),)

    # end class

    class Meta:
        model = models.Administrador
        fields = ['cuenta', 'username', 'password1', 'password2', 'email', 'first_name',
                  'last_name', 'identificacion', 'direccion', 'telefono', 'nacimiento', 'imagen']
        widgets = {
            'cuenta': apply_select2(forms.Select)
        }
    # end class

    def clean(self):
        data = super(AdministradorAdminForm, self).clean()
        if not data.get('cuenta'):
            self.add_error('cuenta', 'Debe seleccionar una cuenta')
        if not data.get('identificacion'):
            self.add_error('identificacion', 'Debe digitar el numero de identificacion.')

    def save(self, commit=True):
        cajero = super(AdministradorAdminForm, self).save(commit)
        cajero.is_staff = True
        cajero.is_superuser = False
        cajero.save()
        usuario = User.objects.filter(id=cajero.id).first()
        grupo = Group.objects.get(name='Administrador')
        if usuario and grupo :
            usuario.groups.add(grupo)
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
        self.fields['nacimiento'].widget = widgets.AdminDateWidget()
        self.fields['telefono'].widget = forms.NumberInput()
    # end def

    class Meta:
        model = models.Administrador
        exclude = ['password1', 'password2', ]
        fields = ['username', 'email', 'first_name',
                  'last_name', 'identificacion', 'direccion', 'telefono', 'nacimiento', 'imagen']
    # end class

    class Media:
        js = ('{}/static/empleados/js/dateoperario.js'.format(SERVER_STATIC),)
    # end class

    def clean(self):
        data = super(AdministradorFormEdit, self).clean()
        if not data.get('identificacion'):
            self.add_error('identificacion', 'Debe digitar el numero de identificacion.')

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


class AdministradorAdminFormEdit(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdministradorAdminFormEdit, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Correo Electrtónico"
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellidos"
        self.fields['nacimiento'].widget = widgets.AdminDateWidget()
        self.fields['telefono'].widget = forms.NumberInput()
    # end def

    class Meta:
        model = models.Administrador
        exclude = ['password1', 'password2', ]
        fields = ['cuenta', 'username', 'email', 'first_name',
                  'last_name', 'identificacion', 'direccion', 'telefono', 'nacimiento', 'imagen']

        widgets = {
            'cuenta': apply_select2(forms.Select)
        }
    # end class

    def clean(self):
        data = super(AdministradorAdminFormEdit, self).clean()
        if not data.get('cuenta'):
            self.add_error('cuenta', 'Debe seleccionar una cuenta')
        if not data.get('identificacion'):
            self.add_error('identificacion', 'Debe digitar el numero de identificacion.')

    class Media:
        js = ('{}/static/empleados/js/dateoperario.js'.format(SERVER_STATIC),)
    # end class

    def save(self, commit=True):
        cajero = super(AdministradorAdminFormEdit, self).save(commit)
        cajero.is_staff = True
        cajero.is_superuser = False
        cajero.save()
        usuario = User.objects.filter(id=cajero.id).first()
        grupo = Group.objects.get(name='Administrador')
        if User.objects.filter(id=cajero.id).first():
            usuario.groups.add(grupo)
        #end if
        return cajero
    # end def
# end class
