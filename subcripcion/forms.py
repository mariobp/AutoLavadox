# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin import widgets
import models
from cuser.middleware import CuserMiddleware
from django.utils import timezone
from datetime import datetime
import pytz

class ModuloForm(forms.ModelForm):
    class Meta:
        model = models.Modulo
        fields = ['nombre','descripcion','estado']
        exclude = []
    #end class

    def save(self, commit=True):
        modulo = super(ModuloForm, self).save(commit)
        modulo.nombre = modulo.nombre.title()
        modulo.save()
        return modulo
    # end def
#end class


class FuncionalidadForm(forms.ModelForm):
    class Meta:
        model = models.Funcionalidad
        fields = ['modulo','nombre','url', 'descripcion', 'estado']
        exclude = []
    #end class

    def save(self, commit=True):
        modulo = super(FuncionalidadForm, self).save(commit)
        modulo.nombre = modulo.nombre.title()
        modulo.save()
        return modulo
    # end def
#end class


class FacturaForm(forms.ModelForm):
    class Meta:
        model = models.Factura
        fields = ['suscripcion','paga', 'estado']
        exclude = []
    #end class

    def save(self, commit=True):
        factura = super(FacturaForm, self).save(commit)
        print 'este es el servicio de factura ',commit
        if factura.paga :
            print 'Factura pagada'
            factura.realizada = timezone.now()
            suscrip = models.Suscripcion.objects.filter(id=factura.suscripcion.id).first()
            if suscrip :
                suscrip.inicio = factura.realizacion
                suscrip.fin = datetime(suscrip.inicio.year, suscrip.inicio.month + suscrip.plan.duracion, suscrip.inicio.day, 23, 59, 59,tzinfo=pytz.UTC)
                print suscrip.fin
                suscrip.save()
            # end if
        #end if
        factura.save()
        return factura
    # end def
#end class


class InstModuloForm(forms.ModelForm):
    class Meta:
        model = models.InstModulo
        fields = ['nombre', 'descripcion', 'modulo', 'funcionalidades', 'estado']
        exclude = []
    #end class

    def save(self, commit=True):
        modulo = super(InstModuloForm, self).save(commit)
        modulo.nombre = modulo.nombre.title()
        modulo.save()
        return modulo
    # end def
#end class


class PlanForm(forms.ModelForm):
    class Meta:
        model = models.Plan
        fields = ['nombre', 'operadores', 'asistentes', 'descripcion', 'valor', 'duracion', 'modulos' ,'estado']
        exclude = []
    #end class

    def save(self, commit=True):
        modulo = super(PlanForm, self).save(commit)
        modulo.nombre = modulo.nombre.title()
        modulo.save()
        return modulo
    # end def
#end class


class ClienteForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar contraseña"
        self.fields['email'].label = "Correo Electrtónico"
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellidos"
    # end def

    def clean(self):
        data = super(ClienteForm, self).clean()
        if data.get('identificacion'):
            if models.Cliente.objects.filter(identificacion=data.get('identificacion')).first():
                self.add_error('identificacion','El cliente se encuentra registrado')
            #end def
    #end def

    class Meta:
        model = models.Cliente
        fields = ['username', 'password1', 'password2', 'email', 'first_name','last_name','identificacion',
         'direccion','telefono']
        exclude = ['estado']
    # end class

    def save(self, commit = True):
        cliente = super(ClienteForm, self).save(commit=False)
        cliente.save()
        cuenta = models.Cuenta(cliente=cliente,estado=True)
        cuenta.save()
        return cliente
    #end def
#end class


class ClienteEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClienteEditForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Correo Electrtónico"
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellidos"
    # end def

    class Meta:
        model = models.Cliente
        fields = ['username', 'email', 'first_name','last_name', 'identificacion',
         'direccion', 'telefono']
        exclude = ['estado', 'password1', 'password2']
    # end class
#end class


class SuscripcionForm(forms.ModelForm):
    class Meta:
        model = models.Suscripcion
        fields = ['plan']
        exclude = ['estado', 'inscripcion', 'inicio','fin','activa']
    # end class

    def __init__(self, request, *args, **kwargs):
        super(SuscripcionForm, self).__init__(*args, **kwargs)
        self.request = request
    #end def

    def clean(self):
        data = super(SuscripcionForm, self).clean()
        if data.get('identificacion'):
            if not models.Cliente.objects.filter(id=data.get('identificacion')).first():
                self.add_error('identificacion','El cliente se encuentra registrado')
            #end def
    #end def

    def save(self, commit = True):
        sucrip = super(SuscripcionForm, self).save(commit=False)
        if commit:
            user = CuserMiddleware.get_user()
            if user:
                cuenta = models.Cuenta.objects.filter(cliente__id=user.id).first()
                if cuenta:
                    sucrip.cuenta = cuenta
                #end if
            #end if
        #conf.empresa= empresa.Empresa.objects.filter(tienda__empleado__user_ptr_id=user.id).first()
        sucrip.save()
        return sucrip
    #end def
#end class


class SuscripcionFormAdmin(forms.ModelForm):
    class Meta:
        model = models.Suscripcion
        fields = '__all__'
        exclude = []
    # end class

    def __init__(self, request, *args, **kwargs):
        super(SuscripcionForm, self).__init__(*args, **kwargs)
        self.request = request
    #end def
#end class
