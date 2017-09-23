# -*- coding: utf-8 -*-
from django import forms
import models
from django_select2.forms import (
    HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
    ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
    Select2Widget
)
from cuser.middleware import CuserMiddleware
from subcripcion import models as suscripcion
from django.db.models import Q
from autolavadox.service import Service
from cliente import models as cliente
from empleados import models as empleado
from autolavadox.forms import BaseForm as Base

class AddTipoServicioForm(Base):
    class Meta:
        model = models.TipoServicio
        fields = ['nombre','costo','comision','vehiculos','state']
        exclude = ['cuenta']
    # end class

    def __init__(self, *args, **kwargs):
        super(AddTipoServicioForm, self).__init__(*args, **kwargs)
        servi = Service.get_instance()
        cuent,user,admin=servi.isUser()
        if cuent and user:
            cuenta=servi.getCuenta()
            self.fields['vehiculos'].queryset = cliente.TipoVehiculo.objects.filter(estado=True,cuenta=cuenta)
        #end if
        print 'cambio el nombre de la etiqueta state'
        self.fields['state'].label="Estado"
    # end def

    def clean(self):
        data = super(AddTipoServicioForm, self).clean()
        print self.add_error
        if not data.get('nombre') :
            self.add_error('nombre', 'El nombre es requerido')
        # end if
        if  data.get('costo') == None :
            self.add_error('costo', 'Digite el costo del servicio.')
        #end if
        if data.get('costo') != None:
            if data.get('costo') < 0 :
                self.add_error('costo', 'El valor debe ser mayor a cero.')
            #end if
        # end if
        if data.get('comision') == None:
            print 'Esto es lo q hay en comision de servicio ',data.get('comision'),' ',(not data.get('comision'))
            self.add_error('comision', 'Digite la comision del servicio.')
        if data.get('comision') != None:
            if data.get('comision') < 0 :
                self.add_error('comision', 'El valor debe ser mayor a cero.')
            #end if
        # end if
        if not data.get('vehiculos') :
            self.add_error('vehiculos', 'Seleccione el tipo de vehiculo.')
        # end if
    # end def
# end class


class AddTipoServicioFormAdmin(Base):
    class Meta:
        model = models.TipoServicio
        fields = ['nombre','costo','comision','vehiculos','cuenta','state']
    # end class

    def __init__(self, *args, **kwargs):
        super(AddTipoServicioFormAdmin, self).__init__(*args, **kwargs)
        servi = Service.get_instance()
        cuent,user,admin=servi.isUser()
        if cuent and user:
            cuenta=servi.getCuenta()
            self.fields['vehiculos'].queryset = cliente.TipoVehiculo.objects.filter(estado=True,cuenta=cuenta)
        #end if
    # end def

    def clean(self):
        data = super(AddTipoServicioFormAdmin, self).clean()
        print self.add_error
        if not data.get('nombre') :
            self.add_error('nombre', 'El nombre es requerido')
        # end if
        if  data.get('costo') :
            if data.get('costo') < 0 :
                self.add_error('costo', 'El valor debe ser mayor a cero.')
            #end if
        # end if
        if not data.get('comision') :
            if data.get('comision') < 0 :
                self.add_error('comision', 'El valor debe ser mayor a cero.')
        # end if
        if not data.get('vehiculos') :
            self.add_error('vehiculos', 'Seleccione el tipo de vehiculo.')
        # end if
    # end def
# end class


class AddOrdenForm(Base):
    class Meta:
        model = models.Orden
        fields = ['recepcionista', 'vehiculo', ]
        exclude = ['fin', 'cajero', 'observacion', 'valor', 'comision', 'numero']
    # end class

    def __init__(self, *args, **kwargs):
        super(AddOrdenForm, self).__init__(*args, **kwargs)
        servi = Service.get_instance()
        cuent,user,admin=servi.isUser()
        if cuent and user:
            cuenta=servi.getCuenta()
            self.fields['vehiculo'].queryset = cliente.Vehiculo.objects.filter(cliente__cuenta=cuenta)
            self.fields['recepcionista'].queryset = empleado.Recepcionista.objects.filter(is_active=True,cuenta=cuenta)
        #end if
    # end def

    def clean(self):
        data = super(AddOrdenForm, self).clean()
        if not data.get('vehiculo') :
            self.add_error('vehiculo', 'Debe seleccionar un vehiculo')
        # end if
    # end def
# end class


class ObservacionOrdenForm(Base):
    class Meta:
        model = models.Orden
        fields = ['observacion', ]
        exclude = ['fin', 'cajero', 'recepcionista', 'valor', 'comision', 'vehiculo']
    # end class
# end class


class AddServicioForm(Base):
    class Meta:
        model = models.Servicio
        fields = ['orden', 'tipo', 'operario']
        exclude = ['valor', 'comision', 'observacion', 'valor', 'estado', 'inicio', 'fin', 'status']
    # end class

    def __init__(self, *args, **kwargs):
        super(AddServicioForm, self).__init__(*args, **kwargs)
        servi = Service.get_instance()
        cuent,user,admin=servi.isUser()
        if cuent and user:
            cuenta=servi.getCuenta()
            self.fields['operario'].queryset = empleado.Empleado.objects.filter(is_active=True,cuenta=cuenta)
            self.fields['tipo'].queryset = models.TipoServicio.objects.filter(state=True,cuenta=cuenta)
        #end if
    # end def

    def clean(self):
        data = super(AddServicioForm, self).clean()
        if not data.get('orden') :
            self.add_error('orden', 'Debe seleccionar la orden')
        # end if
        if not data.get('tipo') :
            self.add_error('tipo', 'Debe seleccionar el tipo de servicio.')
        # end if
    # end def
# end class


class ServicioForm(Base):
    class Meta:
        model = models.Servicio
        exclude = ('vehiculo',)
        fields = {
            'tipo',
            'operario'
        }
        widgets = {
            'tipo': Select2Widget,
            'operario': Select2MultipleWidget
        }
    # end class

    def __init__(self, *args, **kwargs):
        super(ServicioForm, self).__init__(*args, **kwargs)
        servi = Service.get_instance()
        cuent,user,admin=servi.isUser()
        if cuent and user:
            cuenta=servi.getCuenta()
            self.fields['tipo'].queryset = models.TipoServicio.objects.filter(state=True,cuenta=cuenta)
            self.fields['operario'].queryset = empleado.Empleado.objects.filter(is_active=True,cuenta=cuenta)
        #end if
    # end def


    def clean(self):
        data = super(ServicioForm, self).clean()
        if not data.get('tipo') :
            self.add_error('tipo', 'Debe seleccionar el tipo de servicio.')
        # end if
    # end def
# end class


class OrdenForm(Base):
    def __init__(self, *args, **kwargs):
        super(OrdenForm, self).__init__(*args, **kwargs)
        servi = Service.get_instance()
        cuent,user,admin=servi.isUser()
        if cuent and user:
            cuenta=servi.getCuenta()
            self.fields['vehiculo'].queryset = cliente.Vehiculo.objects.filter(cliente__cuenta=cuenta)
            self.fields['recepcionista'].queryset = empleado.Recepcionista.objects.filter(is_active=True,cuenta=cuenta)
        #end if
    # end def

    class Meta:
        model = models.Orden
        exclude = ('valor','recepcionista',)
        fields = {
            'observacion',
            'vehiculo'
        }
        widgets = {
            'vehiculo': Select2Widget,
	    'recepcionista': Select2Widget,
            'observacion': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
        }
    # end class

    def clean(self):
        data = super(OrdenForm, self).clean()
        if not data.get('vehiculo') :
            self.add_error('vehiculo', 'Debe seleccionar un vehiculo')
        # end if
    # end def
# end class
