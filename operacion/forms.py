# -*- coding: utf-8 -*-
from django import forms
import models
from django_select2.forms import (
    HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
    ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
    Select2Widget
)


class AddTipoServicioForm(forms.ModelForm):
    class Meta:
        model = models.TipoServicio
        fields = ['nombre','costo','comision','vehiculos','state']
    # end class

    def clean(self):
        data = super(AddTipoServicioForm, self).clean()
        print self.add_error
        if not data.get('nombre') :
            self.add_error('nombre', 'El nombre es requerido')
        # end if
        if not data.get('costo') :
            self.add_error('costo', 'Digite el costo del servicio.')
        elif data.get('costo') < 0 :
            self.add_error('costo', 'El valor debe ser mayor a cero.')
        # end if
        if not data.get('comision') :
            self.add_error('comision', 'Digite la comision del servicio.')
        elif data.get('comision') < 0 :
            self.add_error('comision', 'El valor debe ser mayor a cero.')
        # end if
        if not data.get('vehiculos') :
            self.add_error('vehiculos', 'Seleccione el tipo de vehiculo.')
        # end if
    # end def
# end class


class AddOrdenForm(forms.ModelForm):
    class Meta:
        model = models.Orden
        fields = ['recepcionista', 'vehiculo', ]
        exclude = ['fin', 'cajero', 'observacion', 'valor', 'comision', ]
    # end class

    def clean(self):
        data = super(AddOrdenForm, self).clean()
        if not data.get('vehiculo') :
            self.add_error('vehiculo', 'Debe seleccionar un vehiculo')
        # end if
    # end def
# end class


class ObservacionOrdenForm(forms.ModelForm):
    class Meta:
        model = models.Orden
        fields = ['observacion', ]
        exclude = ['fin', 'cajero', 'recepcionista', 'valor', 'comision', 'vehiculo']
    # end class
# end class


class AddServicioForm(forms.ModelForm):
    class Meta:
        model = models.Servicio
        fields = ['orden', 'tipo', 'operario']
        exclude = ['valor', 'comision', 'observacion', 'valor', 'estado', 'inicio', 'fin', 'status']
    # end class

    def clean(self):
        data = super(AddServicioForm, self).clean()
        if not data.get('orden') :
            self.add_error('orden', 'Debe seleccionar la orden')
        # end if
        if not data.get('tipo') :
            self.add_error('tipo', 'Debe seleccionar el tipo de servicio.')
        # end if
        if not data.get('operario') :
            self.add_error('operario', 'Debe seleccionar los operarios.')
        # end if
    # end def
# end class


class ServicioForm(forms.ModelForm):
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

    def clean(self):
        data = super(ServicioForm, self).clean()
        if not data.get('tipo') :
            self.add_error('tipo', 'Debe seleccionar el tipo de servicio.')
        # end if
        if not data.get('operario') :
            self.add_error('operario', 'Debe seleccionar los operarios.')
        # end if
    # end def
# end class


class OrdenForm(forms.ModelForm):
    class Meta:
        model = models.Orden
        exclude = ('valor',)
        fields = {
            'observacion',
	    'recepcionista',
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
