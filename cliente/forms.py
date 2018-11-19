# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
from easy_select2 import apply_select2, Select2Multiple
from django.forms.models import BaseInlineFormSet, BaseModelFormSet
import models
from exileui.widgets import DatePickerWidget
from autolavadox.service import Service
from autolavadox.forms import BaseForm
from autolavadox import service


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
        ser = service.Service.get_instance()
        tem_cuenta,is_user,admin = ser.isUser()
        if tem_cuenta and is_user :
            cuenta = ser.getCuenta()
            vehiculo.cuenta = cuenta
            vehiculo.save()
        elif admin:
            print 'Es un super usuario'
        #end if
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
        cuent, user, admin=servi.isUser()
        if cuent and user:
            cuenta=servi.getCuenta()
            self.fields['cliente'].queryset = models.Cliente.objects.filter(cuenta=cuenta)
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
        if tem_cuenta and is_user:
            cuenta = ser.getCuenta()
            cliente.cuenta = cuenta
        elif admin:
            print 'Es un super usuario'
        #end if
        if not cliente.usuario:
            usuario = User.objects.filter(username=cliente.identificacion).first()
            if not usuario:
                usuario = User.objects.create_user(username=cliente.identificacion,
                                                   email='{}@gmail.com'.format(cliente.identificacion),
                                                   password=cliente.identificacion)
                usuario.save()
            cliente.usuario = usuario
        cliente.save()
        return cliente
    # end def
# end class


class AddVehivuloFormAdmin(forms.ModelForm):
    class Meta:
        model = models.Vehiculo
        exclude = ()
        fields = ['cliente', 'tipo', 'placa', 'marca', 'color', 'kilometraje']
        widgets = {
            'tipo': apply_select2(forms.Select),
            'cliente': apply_select2(forms.Select)
        }
    # end class

    def __init__(self, *args, **kwargs):
        super(AddVehivuloFormAdmin, self).__init__(*args, **kwargs)
        servi = Service.get_instance()
        cuent,user,admin=servi.isUser()
        self.cuenta = False
        if self.instance.cliente:
            if self.instance.cliente.cuenta:
                self.cuenta = self.instance.cliente.cuenta
        if admin and self.cuenta:
            cuenta = servi.getCuenta()
            if self.fields.has_key('cliente'):
                self.fields['cliente'].queryset = models.Cliente.objects.filter(cuenta=self.cuenta)
            if self.fields.has_key('tipo'):
                self.fields['tipo'].queryset = models.TipoVehiculo.objects.filter(estado=True, cuenta=self.cuenta)
        else:
            if self.fields.has_key('cliente'):
                self.fields['cliente'].queryset = models.Cliente.objects.all()

    #end def

    def clean(self):
        data = super(AddVehivuloFormAdmin, self).clean()
        if self.fields.has_key('cliente'):
            if not data.get('cliente'):
                self.add_error('cliente', 'Debe seleccionar un cliente.')
        if self.fields.has_key('placa'):
            if not data.get('placa'):
                self.add_error('placa', 'Digite una placa')
            if data.get('placa') and self.cuenta:
                vehiculo = models.Vehiculo.objects.filter(Q(cliente__cuenta=self.cuenta, placa=data.get('placa'))&~Q(id=self.instance.id if self.instance else 0)).first()
                if vehiculo:
                    self.add_error('placa', 'Existe un vehiculo registrado con esta placa.')
        if self.fields.has_key('tipo'):
            if not data.get('tipo'):
                self.add_error('tipo', 'Debe seleccionar un tipo de vehiculo.')


    def save(self, commit=True):
        vehiculo = super(AddVehivuloFormAdmin, self).save(commit)
        if vehiculo.kilometraje:
            historial = models.HistorialKilometraje(vehiculo=vehiculo, kilometraje=vehiculo.kilometraje)
            historial.save()
        # end if
        vehiculo.save()
        return vehiculo
    # end def
# end class


class AddVehivuloFormAd(forms.ModelForm):
    class Meta:
        model = models.Vehiculo
        exclude = ()
        fields = ['cliente', 'tipo', 'placa', 'marca', 'color', 'kilometraje']
        widgets = {
            'tipo': apply_select2(forms.Select),
            'cliente': apply_select2(forms.Select)
        }
    # end class

    def __init__(self, *args, **kwargs):
        super(AddVehivuloFormAd, self).__init__(*args, **kwargs)
        servi = Service.get_instance()
        cuent,user,admin=servi.isUser()
        self.cuenta = None
        if cuent and user:
            self.cuenta=servi.getCuenta()
            self.fields['cliente'].queryset = models.Cliente.objects.filter(cuenta=self.cuenta)
            self.fields['tipo'].queryset = models.TipoVehiculo.objects.filter(estado=True,cuenta=self.cuenta)
        else:
            self.fields['cliente'].queryset = models.Cliente.objects.none()
            self.fields['tipo'].queryset = models.TipoVehiculo.objects.none()
        #end if
    #end def

    def clean(self):
        data = super(AddVehivuloFormAd, self).clean()
        if self.fields.has_key('cliente'):
            if not data.get('cliente'):
                self.add_error('cliente', 'Debe seleccionar un cliente.')
        if self.fields.has_key('placa'):
            if not data.get('placa'):
                self.add_error('placa', 'Digite una placa')
            if data.get('placa') and self.cuenta:
                vehiculo = models.Vehiculo.objects.filter(Q(cliente__cuenta=self.cuenta, placa=data.get('placa'))&~Q(id=self.instance.id if self.instance else 0)).first()
                if vehiculo:
                    self.add_error('placa', 'Existe un vehiculo registrado con esta placa.')
        if self.fields.has_key('tipo'):
            if not data.get('tipo'):
                self.add_error('tipo', 'Debe seleccionar un tipo de vehiculo.')

    def save(self, commit=True):
        vehiculo = super(AddVehivuloFormAd, self).save(commit)
        if vehiculo.kilometraje:
            historial = models.HistorialKilometraje(vehiculo=vehiculo, kilometraje=vehiculo.kilometraje)
            historial.save()
        # end if
        vehiculo.save()
        return vehiculo
    # end def
# end class


class AddCliente(BaseForm):
    def __init__(self, *args, **kwargs):
        super(AddCliente, self).__init__(*args, **kwargs)
        self.fields['dirreccion'].label = "Dirección "
        self.fields['nacimiento'].widget = DatePickerWidget(
            attrs={'class': 'dateclien'},
            format="%d/%m/%Y")

        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        self.cuenta = ser.getCuenta()
    # end def

    class Media:
        js = ('/static/cliente/js/clienteadd.js',)
    # end class

    class Meta:
        model = models.Cliente
        fields = ['identificacion', 'nombre', 'apellidos', 'dirreccion', 'correo',
                  'celular', 'nacimiento']
    # end class

    def clean(self):
        data = super(AddCliente, self).clean()
        if data.get('identificacion'):
            cliente = models.Cliente.objects.filter(Q(identificacion=data.get('identificacion'),  cuenta=self.cuenta) & ~Q(id=self.instance.id if self.instance else 0)).first()
            if cliente:
                self.add_error('identificacion', 'Existe un cliente registrado con este documento.')


    def save(self, commit=True):
        cliente = super(AddCliente, self).save(commit)
        ser = Service.get_instance()
        tem_cuenta,is_user,admin = ser.isUser()
        if tem_cuenta and is_user:
            cuenta = ser.getCuenta()
            cliente.cuenta = cuenta
        elif admin:
            print 'Es un super usuario'
        #end if
        if not cliente.usuario and cliente.identificacion:
            usuario = User.objects.filter(username=cliente.identificacion).first()
            if not usuario:
                usuario = User.objects.create_user(username=cliente.identificacion,
                                                   email=cliente.correo if cliente.correo else '{}@gmail.com'.format(cliente.identificacion),
                                                   password=cliente.identificacion)
                usuario.save()
            cliente.usuario = usuario
        cliente.save()
        return cliente
    # end def
# end class


class AddClienteAdmin(BaseForm):
    def __init__(self, *args, **kwargs):
        super(AddClienteAdmin, self).__init__(*args, **kwargs)
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
        fields = ['cuenta', 'identificacion', 'nombre', 'apellidos', 'dirreccion', 'correo',
                  'celular', 'nacimiento']

        widgets = {
            'cuenta': apply_select2(forms.Select)
        }
    # end class

    def clean(self):
        data = super(AddClienteAdmin, self).clean()
        if data.get('identificacion') and data.get('cuenta'):
            cliente = models.Cliente.objects.filter(Q(identificacion=data.get('identificacion'), cuenta=data.get('cuenta'))&~Q(id=self.instance.id if self.instance else 0)).first()
            if cliente:
                self.add_error('identificacion', 'Existe un cliente registrado con este documento.')
        if not data.get('cuenta'):
            self.add_error('cuenta', 'Debe seleccionar una cuenta.')

    def save(self, commit=True):
        cliente = super(AddClienteAdmin, self).save(commit)
        if not cliente.usuario and cliente.identificacion:
            usuario = User.objects.filter(username=cliente.identificacion).first()
            if not usuario:
                usuario = User.objects.create_user(username=cliente.identificacion,
                                                   email=cliente.correo if cliente.correo else '{}@gmail.com'.format(cliente.identificacion),
                                                   password=cliente.identificacion)
                usuario.save()
            cliente.usuario = usuario
        cliente.save()
        return cliente
    # end def
# end class

class TipoServicioForm(forms.ModelForm):
    class Meta:
        model = models.TipoVehiculo
        fields = ['nombre', 'descripcion']
        exclude = ['estado','cuenta']
        widgets = {
            'descripcion': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
        }
    # end class

    def __init__(self, *args, **kwargs):
        super(TipoServicioForm, self).__init__(*args, **kwargs)
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        self.cuenta = None
        if tem_cuenta and is_user:
            self.cuenta = ser.getCuenta()

    def save(self, commit=True):
        data = super(TipoServicioForm, self).save(commit)
        if self.cuenta:
            data.cuenta = self.cuenta
            data.save()
        return data
    #end def


    def clean(self):
        data = super(TipoServicioForm, self).clean()
        if not data.get('nombre'):
            self.add_error('nombre', 'Debe digitar el nombre.')
        elif data.get('nombre'):
            tipo = models.TipoVehiculo.objects.filter(Q(cuenta=self.cuenta, nombre=data.get('nombre')) & ~Q(id=self.instance.id if self.instance else 0))
            if tipo:
                self.add_error('nombre', 'El nombre existe registrado.')

# end class


class TipoServicioFormAdmin(forms.ModelForm):
    class Meta:
        model = models.TipoVehiculo
        fields = ['cuenta', 'nombre', 'descripcion']
        exclude = ['estado']
        widgets = {
            'descripcion':  forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'cuenta': apply_select2(forms.Select),
        }
    # end class

    def clean(self):
        data = super(TipoServicioFormAdmin, self).clean()
        if not data.get('cuenta'):
            self.add_error('cuenta', 'Debe seleccionar una Cuenta.')
        if not data.get('nombre'):
            self.add_error('nombre', 'Debe digitar el nombre.')
        elif data.get('cuenta') and data.get('nombre'):
            tipo = models.TipoVehiculo.objects.filter(Q(cuenta=data.get('cuenta'), nombre=data.get('nombre')) & ~Q(id=self.instance.id if self.instance else 0))
            if tipo:
                self.add_error('nombre', 'El nombre existe registrado.')
# end class
