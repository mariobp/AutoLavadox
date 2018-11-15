# -*- coding: utf-8 -*-
from django import forms
import models
from exileui.widgets import DatePickerWidget
from autolavadox import service
from django.db.models import Q
from django.contrib.admin import widgets
from autolavadox.settings import SERVER_STATIC
from easy_select2 import apply_select2, Select2Multiple

class BaseForm(forms.ModelForm):
    def save(self, commit=True):
        data = super(BaseForm, self).save(commit)
        data.save()
        ser = service.Service.get_instance()
        tem_cuenta,is_user,admin = ser.isUser()
        if tem_cuenta and is_user :
            cuenta = ser.getCuenta()
            data.cuenta = cuenta
        elif admin:
            print 'Es un super usuario'
        #end if
        data.save()
        return data
    #end def
#end class

class AddTipoServicioForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(AddTipoServicioForm, self).__init__(*args, **kwargs)
        self.fields['inicio'].widget = widgets.AdminTimeWidget()
        self.fields['fin'].widget = widgets.AdminTimeWidget()
    # end def

    def clean(self):
        data = super(AddTipoServicioForm, self).clean()
        print data,data.get('fin')
        if not data.get('fin') :
            self.add_error('fin', 'Debe digitar la fecha de fin de reporte')
        # end if
        if not data.get('inicio') :
            self.add_error('fin', 'Debe digitar la fecha de fin de reporte')
        # end if
        if data.get('fin')   and data.get('inicio')  :
            if data.get('fin') < data.get('inicio') :
                self.add_error('inicio', 'La fecha de inio debe ser menor a la de fin')
            # end if
        #end if
    # end def

    class Media:
        js = ('{}/static/cierre/js/date.js'.format(SERVER_STATIC),)
    # end class

    class Meta:
        model = models.TipoServicio
        fields = ['inicio', 'fin']
        exclude = ['total',]
    # end class
# end class


class AddFacturaForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(AddTipoServicioForm, self).__init__(*args, **kwargs)
        self.fields['inicio'].widget = widgets.AdminTimeWidget()
        self.fields['fin'].widget = widgets.AdminTimeWidget()
    # end def

    class Media:
        js = ('{}/static/cierre/js/date.js'.format(SERVER_STATIC),)
    # end class

    class Meta:
        model = models.Factura
        fields = ['inicio', 'fin']
        exclude = ['total',]
    # end class

    def clean(self):
        data = super(AddFacturaForm, self).clean()
        if not data.get('fin') :
            self.add_error('fin', 'Debe digitar la fecha de fin de reporte')
        # end if
        if not data.get('inicio') :
            self.add_error('fin', 'Debe digitar la fecha de fin de reporte')
        # end if
        if data.get('fin') and data.get('inicio'):
            if data.get('fin') < data.get('inicio') :
                self.add_error('inicio', 'La fecha de inio debe ser menor a la de fin')
            # end if
        #end if
    # end def
# end class


class TurnoAdminForm(forms.ModelForm):
    class Meta:
        model = models.Turno
        fields = ['cuenta', 'nombre', 'inicio', 'fin']

    def __init__(self, *args, **kwargs):
        super(TurnoAdminForm, self).__init__(*args, **kwargs)
        self.fields['inicio'].widget = widgets.AdminTimeWidget()
        self.fields['fin'].widget = widgets.AdminTimeWidget()

    def clean(self):
        data = super(TurnoAdminForm, self).clean()
        if not data.get('cuenta'):
            self.add_error('cuenta', 'Debe seleccionar una cuenta.')
        if not data.get('nombre'):
            self.add_error('nombre', 'Debe digitar un nombre.')
        elif data.get('nombre') and data.get('cuenta'):
            tipo = models.Turno.objects.filter(Q(cuenta=data.get('cuenta'), nombre=data.get('nombre'))&~Q(id=self.instance.id if self.instance else 0)).first()
            if tipo:
                self.add_error('nombre', 'El nombre se encuentra registrado')
        if data.get('inicio') and data.get('fin') and data.get('cuenta'):
            turno = models.Turno.objects.filter(Q(cuenta=data.get('cuenta'), inicio__lte=data.get('inicio'), fin__gt=data.get('inicio'))|
                                                Q(cuenta=data.get('cuenta'), inicio__lte=data.get('fin'), fin__gt=data.get('fin'))).first()
            if turno:
                self.add_error('inicio', 'El intervalo no se encuentra disponible.')


class TurnoForm(BaseForm):
    class Meta:
        model = models.Turno
        fields = ['nombre', 'inicio', 'fin']

    def __init__(self, *args, **kwargs):
        super(TurnoForm, self).__init__(*args, **kwargs)
        self.fields['inicio'].widget = widgets.AdminTimeWidget()
        self.fields['fin'].widget = widgets.AdminTimeWidget()
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        self.cuenta = None
        if tem_cuenta and is_user:
            self.cuenta = ser.getCuenta()

    def clean(self):
        data = super(TurnoForm, self).clean()
        if not data.get('nombre'):
            self.add_error('nombre', 'Debe digitar un nombre.')
        elif data.get('nombre') and self.cuenta:
            tipo = models.Turno.objects.filter(Q(cuenta=self.cuenta, nombre=data.get('nombre'))&~Q(id=self.instance.id if self.instance else 0)).first()
            if tipo:
                self.add_error('nombre', 'El nombre se encuentra registrado')
        if data.get('inicio') and data.get('fin') and self.cuenta:
            turno = models.Turno.objects.filter(Q(cuenta=self.cuenta, inicio__lte=data.get('inicio'), fin__gt=data.get('inicio'))&
                                                Q(cuenta=self.cuenta, inicio__lte=data.get('fin'), fin__gt=data.get('fin'))).first()
            if turno:
                self.add_error('inicio', 'El intervalo no se encuentra disponible')


class CierreAdminForm(forms.ModelForm):
    class Meta:
        model = models.Cierre
        fields = ['cuenta', 'turno', 'total', 'comision', 'inicio', 'fin']
        widgets = {
            'turno': apply_select2(forms.Select)
        }

    def __init__(self, *args, **kwargs):
        super(CierreAdminForm, self).__init__(*args, **kwargs)
        if self.fields.has_key('inicio'):
            self.fields['inicio'].widget = widgets.AdminDateWidget()
        if self.fields.has_key('fin'):
            self.fields['fin'].widget = widgets.AdminDateWidget()
        if self.fields.has_key('turno'):
            if self.instance.cuenta:
                self.fields['turno'].queryset = models.Turno.objects.filter(cuenta=self.instance.cuenta)
            else:
                self.fields['turno'].queryset = models.Turno.objects.none()


    def clean(self):
        data = super(CierreAdminForm, self).clean()
        if self.fields.has_key('cuenta'):
            if not data.get('cuenta'):
                self.add_error('cuenta', 'Debe seleccionar una cuenta.')
        if self.fields.has_key('turno'):
            if not data.get('turno'):
                self.add_error('turno', 'Debe seleccionar un turno.')
        if self.fields.has_key('nombre'):
            if not data.get('nombre'):
                self.add_error('nombre', 'Debe digitar un nombre.')
            elif data.get('nombre') and self.instance.cuenta:
                tipo = models.Cierre.objects.filter(Q(cuenta=self.instance.cuenta, nombre=data.get('nombre'))&~Q(id=self.instance.id if self.instance else 0)).first()
                if tipo:
                    self.add_error('nombre', 'El nombre se encuentra registrado')
        if self.fields.has_key('inicio') and self.fields.has_key('fin'):
            if not data.get('inicio'):
                self.add_error('inicio', 'Debe digitar la fecha de inicio')
            if not data.get('fin'):
                self.add_error('fin', 'Debe digitar la fecha de fin.')
            if data.get('inicio') and data.get('fin'):
                if data.get('inicio') > data.get('fin'):
                    self.add_error('inicio', 'La fecha de inicio debe ser mayor de la final.')
                elif self.instance.cuenta:
                    turno = models.Cierre.objects.filter(Q(cuenta=self.instance.cuenta, inicio__lte=data.get('inicio'), fin__gt=data.get('inicio'))|
                                                        Q(cuenta=self.instance.cuenta, inicio__lte=data.get('fin'), fin__gt=data.get('fin'))).first()
                    if turno:
                        self.add_error('inicio', 'El intervalo no se encuentra disponible.')


class CierreForm(BaseForm):
    class Meta:
        model = models.Cierre
        fields = ['turno', 'total', 'comision', 'inicio', 'fin']
        widgets = {
            'turno': apply_select2(forms.Select)
        }

    def __init__(self, *args, **kwargs):
        super(CierreForm, self).__init__(*args, **kwargs)
        self.fields['inicio'].widget = widgets.AdminDateWidget()
        self.fields['fin'].widget = widgets.AdminDateWidget()
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        self.cuenta = None
        if tem_cuenta and is_user:
            self.cuenta = ser.getCuenta()

    def clean(self):
        data = super(CierreForm, self).clean()
        if self.fields.has_key('cuenta'):
            if not data.get('cuenta'):
                self.add_error('cuenta', 'Debe seleccionar una cuenta.')
        if self.fields.has_key('turno'):
            if not data.get('turno'):
                self.add_error('turno', 'Debe seleccionar un turno.')
        if self.fields.has_key('nombre'):
            if not data.get('nombre'):
                self.add_error('nombre', 'Debe digitar un nombre.')
            elif data.get('nombre') and self.cuenta:
                tipo = models.Cierre.objects.filter(Q(cuenta=self.cuenta, nombre=data.get('nombre'))&~Q(id=self.instance.id if self.instance else 0)).first()
                if tipo:
                    self.add_error('nombre', 'El nombre se encuentra registrado')
        if self.fields.has_key('inicio') and self.fields.has_key('fin'):
            if not data.get('inicio'):
                self.add_error('inicio', 'Debe digitar la fecha de inicio')
            if not data.get('fin'):
                self.add_error('fin', 'Debe digitar la fecha de fin.')
            if data.get('inicio') and data.get('fin'):
                if data.get('inicio') > data.get('fin'):
                    self.add_error('inicio', 'La fecha de inicio debe ser mayor de la final.')
                elif self.instance.cuenta:
                    turno = models.Cierre.objects.filter(Q(cuenta=self.cuenta, inicio__lte=data.get('inicio'), fin__gt=data.get('inicio'))|
                                                        Q(cuenta=self.cuenta, inicio__lte=data.get('fin'), fin__gt=data.get('fin'))).first()
                    if turno:
                        self.add_error('inicio', 'El intervalo no se encuentra disponible.')