# -*- coding: utf-8 -*-
from django import forms
from easy_select2 import apply_select2, Select2Multiple
from django.forms.models import BaseInlineFormSet, BaseModelFormSet
import models
from django_select2.forms import (
    HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
    ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
    Select2Widget
)
from cuser.middleware import CuserMiddleware

from autolavadox import service
from subcripcion import models as suscripcion
from django.db.models import Q
from autolavadox.service import Service
from cliente import models as cliente
from empleados import models as empleado
from autolavadox.forms import BaseForm as Base
from inventario import models as inventario


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
        fields = ['nombre','costo','comision', 'cuenta', 'vehiculos','state']
        widgets = {
            'cuenta': apply_select2(forms.Select),
        }
    # end class

    def __init__(self, *args, **kwargs):
        super(AddTipoServicioFormAdmin, self).__init__(*args, **kwargs)
        if self.fields.has_key('vehiculos'):
            self.fields['vehiculos'].queryset = cliente.TipoVehiculo.objects.filter(estado=True,cuenta=self.instance.cuenta)
        #end if
    # end def

    def clean(self):
        data = super(AddTipoServicioFormAdmin, self).clean()
        if self.fields.has_key('nombre'):
            if not data.get('nombre'):
                self.add_error('nombre', 'El nombre es requerido')
            elif data.get('nombre'):
                tipo = models.TipoServicio.objects.filter(Q(cuenta= self.instance.cuenta, nombre=data.get('nombre'))&~Q(id=self.instance.id if self.instance else 0)).first()
                if tipo:
                    self.add_error('nombre', 'El nombre se encuentra registrado.')
        if self.fields.has_key('costo'):
            if data.get('costo') :
                if data.get('costo') < 0 :
                    self.add_error('costo', 'El valor debe ser mayor a cero.')
                #end if
            # end if
        if self.fields.has_key('comision'):
            if not data.get('comision') :
                if data.get('comision') < 0 :
                    self.add_error('comision', 'El valor debe ser mayor a cero.')
            # end if
        if self.fields.has_key('vehiculos'):
            if not data.get('vehiculos') :
                self.add_error('vehiculos', 'Seleccione el tipo de vehiculo.')
            # end if
    # end def
# end class


class AddOrdenForm(forms.ModelForm):
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

    def save(self, commit=True):
        data = super(AddOrdenForm, self).save(commit)
        data.save()
        ser = service.Service.get_instance()
        tem_cuenta,is_user,admin = ser.isUser()
        if tem_cuenta and is_user :
            cuenta = ser.getCuenta()
            data.cuenta = cuenta
            if data.turno == 0:
                data.turno = cuenta.cliente.turnero + 1
                cuenta.cliente.turnero = data.turno
                cuenta.cliente.save()
        elif admin:
            print 'Es un super usuario'
        #end if
        data.save()
        return data
    #end def
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
        if not data.get('orden'):
            self.add_error('orden', 'Debe seleccionar la orden')
        # end if
        if not data.get('tipo'):
            self.add_error('tipo', 'Debe seleccionar el tipo de servicio.')
        # end if
    # end def
# end class


class ServicioForm(Base):
    class Meta:
        model = models.Servicio
        exclude = ()
        fields = {
            'tipo',
            'orden',
            'operario',
        }
        widgets = {
            'tipo': apply_select2(forms.Select),
            'orden': apply_select2(forms.Select),
            'operario': Select2Multiple
        }
    # end class

    def __init__(self, *args, **kwargs):
        super(ServicioForm, self).__init__(*args, **kwargs)
        ser = service.Service.get_instance()
        self.cuenta = ser.getCuenta()
        if self.cuenta:
            self.fields['tipo'].queryset = models.TipoServicio.objects.filter(state=True, cuenta=self.cuenta)
            self.fields['operario'].queryset = empleado.Empleado.objects.filter(is_active=True, cuenta=self.cuenta)
    # end def


    def clean(self):
        data = super(ServicioForm, self).clean()
        if not data.get('tipo') :
            self.add_error('tipo', 'Debe seleccionar el tipo de servicio.')
        # end if
    # end def

    def save(self, commit=True):
        servicio = super(ServicioForm, self).save(commit)
        if self.fields.has_key('tipo'):
            servicio.valor = servicio.tipo.costo
            servicio.comision = servicio.tipo.costo * servicio.tipo.comision
            servicio.save()
        return servicio
# end class


class ServicioInlineForm(Base):
    class Meta:
        model = models.Servicio
        exclude = ()
        fields = {
            'tipo',
            'orden',
            'operario',
            'estado',
        }
        widgets = {
            'tipo': apply_select2(forms.Select),
            'orden': apply_select2(forms.Select),
            'operario': Select2Multiple
        }
    # end class

    def __init__(self, *args, **kwargs):
        self.orden = kwargs.pop('orden')
        super(ServicioInlineForm, self).__init__(*args, **kwargs)
        if self.orden.cuenta:
            self.fields['tipo'].queryset = models.TipoServicio.objects.filter(state=True, cuenta=self.orden.cuenta)
            self.fields['operario'].queryset = empleado.Empleado.objects.filter(is_active=True, cuenta=self.orden.cuenta)
        else:
            self.fields['tipo'].queryset = models.TipoServicio.objects.none()
            self.fields['operario'].queryset = empleado.Empleado.objects.none()
    # end def


    def clean(self):
        data = super(ServicioInlineForm, self).clean()
        if not data.get('tipo'):
            self.add_error('tipo', 'Debe seleccionar el tipo de servicio.')
        # end if
    # end def

    def save(self, commit=True):
        servicio = super(ServicioInlineForm, self).save(commit)
        if self.fields.has_key('tipo'):
            servicio.valor = servicio.tipo.costo
            servicio.comision = servicio.tipo.costo * servicio.tipo.comision
            servicio.save()
        return servicio
# end class


class ServicioAdminForm(forms.ModelForm):
    class Meta:
        model = models.Servicio
        exclude = ()
        fields = [
            'cuenta',
            'orden',
            'tipo',
            'operario',
        ]
        widgets = {
            'cuenta': apply_select2(forms.Select),
            'tipo': apply_select2(forms.Select),
            'orden': apply_select2(forms.Select),
            'operario': Select2Multiple,
        }
    # end class

    def __init__(self, *args, **kwargs):
        super(ServicioAdminForm, self).__init__(*args, **kwargs)
        print 'esta desde la clase de servicio adminSS ', self.instance
        if self.instance:
            if self.instance.cuenta:
                self.fields['tipo'].queryset = models.TipoServicio.objects.filter(state=True, cuenta=self.instance.cuenta)
                self.fields['operario'].queryset = empleado.Empleado.objects.filter(is_active=True, cuenta=self.instance.cuenta)

    # end def

    def clean(self):
        data = super(ServicioAdminForm, self).clean()
        if self.fields.has_key('tipo'):
            if not data.get('tipo') :
                self.add_error('tipo', 'Debe seleccionar el tipo de servicio.')
            # end if
        if self.fields.has_key('cuenta'):
            if not data.get('cuenta'):
                self.add_error('cuenta', 'Dese seleccionar una cuenta.')
    # end def

    def save(self, commit=True):
        servicio = super(ServicioAdminForm, self).save(commit)
        if self.fields.has_key('tipo'):
            servicio.valor = servicio.tipo.costo
            servicio.comision = servicio.tipo.costo * servicio.tipo.comision
            servicio.save()
        return servicio
# end class


class OrdenForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrdenForm, self).__init__(*args, **kwargs)
        servi = Service.get_instance()
        cuent, user, admin = servi.isUser()
        existe = False
        if cuent and user and self.fields.has_key('vehiculo') and self.fields.has_key('recepcionista'):
            self.cuenta=servi.getCuenta()
            self.fields['vehiculo'].queryset = cliente.Vehiculo.objects.filter(cliente__cuenta=self.cuenta)
            self.fields['recepcionista'].queryset = empleado.Recepcionista.objects.filter(is_active=True, cuenta=self.cuenta)
            existe = True
        if not existe and self.fields.has_key('vehiculo') and self.fields.has_key('recepcionista'):
            self.fields['vehiculo'].queryset = cliente.Vehiculo.objects.none()
            self.fields['recepcionista'].queryset = empleado.Recepcionista.objects.none()
        # end def

    class Meta:
        model = models.Orden
        exclude = ('valor','recepcionista',)
        fields = {
            'observacion',
            'vehiculo'
        }
        widgets = {
            'vehiculo': apply_select2(forms.Select)
        }
    # end class

    def save(self, commit=True):
        data = super(OrdenForm, self).save(commit)
        data.save()
        ser = service.Service.get_instance()
        tem_cuenta,is_user,admin = ser.isUser()
        if tem_cuenta and is_user :
            cuenta = ser.getCuenta()
            data.cuenta = cuenta
            if data.turno == 0:
                data.turno = cuenta.cliente.turnero + 1
                cuenta.cliente.turnero = data.turno
                cuenta.cliente.save()
        elif admin:
            print 'Es un super usuario'
        #end if
        data.save()
        return data
    #end def

    def clean(self):
        data = super(OrdenForm, self).clean()
        if not data.get('vehiculo') :
            self.add_error('vehiculo', 'Debe seleccionar un vehiculo')
        # end if
    # end def
# end class


class OrdenAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrdenAdminForm, self).__init__(*args, **kwargs)

        if self.instance.cuenta:
            if self.fields.has_key('vehiculo'):
                self.fields['vehiculo'].queryset = cliente.Vehiculo.objects.filter(cliente__cuenta=self.instance.cuenta)
            if self.fields.has_key('recepcionista'):
                self.fields['recepcionista'].queryset = empleado.Recepcionista.objects.filter(is_active=True,cuenta=self.instance.cuenta)
        #end if
    # end def

    class Meta:
        model = models.Orden
        exclude = ('valor',)
        fields = {
            'observacion',
            'vehiculo',
            'recepcionista',
            'cuenta',
        }
        widgets = {
            'vehiculo': apply_select2(forms.Select),
            'cuenta': apply_select2(forms.Select)
        }
    # end class

    def save(self, commit=True):
        data = super(OrdenAdminForm, self).save(commit)
        if data.cuenta:
            if data.turno == 0:
                data.turno = data.cuenta.cliente.turnero + 1
                data.cuenta.cliente.turnero = data.turno
                data.cuenta.cliente.save()
        data.save()
        return data
    #end def
# end class


class OrdenEditForm(Base):
    def __init__(self, *args, **kwargs):
        super(OrdenEditForm, self).__init__(*args, **kwargs)
        servi = Service.get_instance()
        cuent,user,admin=servi.isUser()
        if cuent and user:
            cuenta=servi.getCuenta()
            self.fields['vehiculo'].queryset = cliente.Vehiculo.objects.filter(cliente__cuenta=cuenta)
            if self.fields.has_key('recepcionista'):
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
    # end class

    def clean(self):
        data = super(OrdenEditForm, self).clean()
        if not data.get('vehiculo') :
            self.add_error('vehiculo', 'Debe seleccionar un vehiculo')
        # end if
    # end def
# end class


class SerivioInlineFormset(BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        kwargs.update({'orden': self.instance})
        form = super(SerivioInlineFormset, self)._construct_form(i, **kwargs)
        return form

    @property
    def empty_form(self):
        kwargs = {'orden': self.instance}
        form = self.form(
            auto_id=self.auto_id,
            prefix=self.add_prefix('__prefix__'),
            empty_permitted=True,
            **kwargs
        )
        self.add_fields(form, None)
        return form


class ComposicionServicioForm(forms.ModelForm):
    class Meta:
        model = models.ComposicionServicio
        fields = ['servicio']
        exclude = ['cuenta']
        widgets = {
            'cuenta': apply_select2(forms.Select),
            'servicio': apply_select2(forms.Select),
        }

    def __init__(self, *args, **kwargs):
        super(ComposicionServicioForm, self).__init__(*args, **kwargs)
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        self.cuenta = ser.getCuenta()
        if not admin and self.fields.has_key('servicio'):
            self.fields['servicio'].queryset = models.TipoServicio.objects.filter(Q(composicionservicio__isnull=True, cuenta=self.cuenta)|Q(id=self.instance.servicio.id if self.instance.servicio else 0))

    def clean(self):
        data = super(ComposicionServicioForm, self).clean()
        if not data.get('servicio'):
            self.add_error('servicio', 'Debe seleccionar un servicio.')

    def save(self, commit=True):
        composicion = super(ComposicionServicioForm, self).save(commit)
        composicion.cuenta = self.cuenta
        composicion.save()
        return composicion


class ComposicionServicioAdminForm(forms.ModelForm):
    class Meta:
        model = models.ComposicionServicio
        fields = ['servicio', 'cuenta']
        widgets = {
            'cuenta': apply_select2(forms.Select),
            'servicio': apply_select2(forms.Select),
        }

    def __init__(self, *args, **kwargs):
        super(ComposicionServicioAdminForm, self).__init__(*args, **kwargs)
        if self.fields.has_key('servicio') and self.instance.cuenta:
            self.fields['servicio'].queryset = models.TipoServicio.objects.filter(Q(composicionservicio__isnull=True, cuenta=self.instance.cuenta)|Q(id=self.instance.servicio.id if self.instance.servicio else 0))

    def clean(self):
        data = super(ComposicionServicioAdminForm, self).clean()
        if data.has_key('servicio'):
            if not data.get('servicio'):
                self.add_error('servicio', 'Debe seleccionar un servicio.')


class ComponenteInlineFormset(BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        kwargs.update({'composicion_servicio': self.instance})
        form = super(ComponenteInlineFormset, self)._construct_form(i, **kwargs)
        return form

    @property
    def empty_form(self):
        kwargs = {'composicion_servicio': self.instance}
        form = self.form(
            auto_id=self.auto_id,
            prefix=self.add_prefix('__prefix__'),
            empty_permitted=True,
            **kwargs
        )
        self.add_fields(form, None)
        return form


class ComponenteInlineForm(forms.ModelForm):
    class Meta:
        model = models.Componente
        fields = ['composicion', 'producto', 'cantidad']
        exclude = ['cuenta']

    def __init__(self, *args, **kwargs):
        self.composicion_servicio = kwargs.pop('composicion_servicio')
        super(ComponenteInlineForm, self).__init__(*args, **kwargs)
        switch = False
        if self.composicion_servicio:
            if self.composicion_servicio.cuenta:
                self.fields['producto'].queryset = inventario.Operacion.objects.filter(cuenta=self.composicion_servicio.cuenta)
                switch=True
        if not switch:
            self.fields['producto'].queryset = inventario.Operacion.objects.none()

    def clean(self):
        data = super(ComponenteInlineForm, self).clean()
        if data.get('cantidad'):
            if data.get('cantidad') < 0:
                self.add_error('cantidad', 'La cantidad debe ser mayor a cero.')

    def save(self, commit=True):
        componente = super(ComponenteInlineForm, self).save(commit)
        if self.composicion_servicio.cuenta:
            componente.cuenta = self.composicion_servicio.cuenta
            componente.save()
        return componente


class ComponenteForm(forms.ModelForm):
    class Meta:
        model = models.Componente
        fields = ['composicion', 'producto', 'cantidad']
        exclude = ['cuenta']

    def __init__(self, *args, **kwargs):
        super(ComponenteForm, self).__init__(*args, **kwargs)
        ser = service.Service.get_instance()
        self.cuenta= ser.getCuenta()
        if self.cuenta:
            self.fields['producto'].queryset = inventario.Operacion.objects.filter(cuenta=self.cuenta)
            self.fields['composicion'].queryset = self.cuenta.composicionservicio_set.all()
        else:
            self.fields['producto'].queryset = inventario.Operacion.objects.none()
            self.fields['composicion'].queryset = models.ComposicionServicio.objects.none()

    def clean(self):
        data = super(ComponenteForm, self).clean()
        if data.get('cantidad'):
            if data.get('cantidad') < 0:
                self.add_error('cantidad', 'La cantidad debe ser mayor a cero.')
        if not data.get('producto'):
            self.add_error('producto', 'Debe seleccionar un prodicto.')
        if not data.get('composicion'):
            self.add_error('composicion', 'Debe seleccionar una composicion')

    def save(self, commit=True):
        componente = super(ComponenteForm, self).save(commit)
        if self.cuenta:
            componente.cuenta = self.cuenta
            componente.save()
        return componente


class ComponenteAdminForm(forms.ModelForm):
    class Meta:
        model = models.Componente
        fields = ['cuenta', 'composicion', 'producto', 'cantidad']

    def __init__(self, *args, **kwargs):
        super(ComponenteAdminForm, self).__init__(*args, **kwargs)
        entro_p = False
        entro_c = False
        if self.instance.cuenta:
            if self.fields.has_key('producto'):
                self.fields['producto'].queryset = inventario.Operacion.objects.filter(cuenta=self.instance.cuenta)
                entro_p = True
            if self.fields.has_key('composicion'):
                self.fields['composicion'].queryset = self.instance.cuenta.composicionservicio_set.all()
                entro_c = True
        if not entro_p:
            if self.fields.has_key('productos'):
                self.fields['productos'].queryset = inventario.Operacion.objects.none()
        if not entro_c:
            if self.fields.has_key('composicion'):
                self.fields['composicion'].queryset = models.ComposicionServicio.objects.none()

    def clean(self):
        data = super(ComponenteAdminForm, self).clean()
        if data.get('cantidad'):
            if data.get('cantidad') < 0:
                self.add_error('cantidad', 'La cantidad debe ser mayor a cero.')
        if self.fields.has_key('producto'):
            if not data.get('producto'):
                self.add_error('producto', 'Debe seleccionar un prodicto.')
        if self.fields.has_key('composicion'):
            if not data.get('composicion'):
                self.add_error('composicion', 'Debe seleccionar una composicion')


class ProductoVentaInlineFormset(BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        kwargs.update({'orden': self.instance})
        form = super(ProductoVentaInlineFormset, self)._construct_form(i, **kwargs)
        return form

    @property
    def empty_form(self):
        kwargs = {'orden': self.instance}
        form = self.form(
            auto_id=self.auto_id,
            prefix=self.add_prefix('__prefix__'),
            empty_permitted=True,
            **kwargs
        )
        self.add_fields(form, None)
        return form


class ProductoVentaInlineForm(forms.ModelForm):
    class Meta:
        model = models.ProductoVenta
        fields = ['orden', 'producto', 'cantidad']
        exclude = ['total', 'cuenta']

    def __init__(self, *args, **kwargs):
        self.orden = kwargs.pop('cuenta')
        super(ProductoVentaInlineForm, self).__init__(*args, **kwargs)
        existe = False
        if self.orden:
            if self.orden.cuanta:
                self.fields['producto'].queryset = inventario.Venta.objects.filter(cuenta=self.orden.cuenta)
                existe= True
        if not existe:
            self.fields['producto'].queryset = inventario.Venta.objects.none()

    def clean(self):
        data = super(ProductoVentaInlineForm, self).clean()
        if not data.get('servicio'):
            self.add_error('producto', 'Debe seleccionar un producto.')
        if data.get('producto'):
            if data.get('producto') < 0:
                self.data('La cantidad  debe ser mayor o igual a cero')

    def save(self, commit=True):
        producto = super(ProductoVentaInlineForm, self).save(commit)
        exist = False
        if self.orden:
            if self.orden.cuenta:
                producto.cuenta = self.orden.cuenta
                exist = True
        if producto.producto:
            producto.total = producto.producto.precio_venta
            exist = True
        if exist:
            producto.save()
        return producto


class ProductoVentaInlineForm(forms.ModelForm):
    class Meta:
        model = models.ProductoVenta
        fields = ['orden', 'producto', 'cantidad']
        exclude = ['total', 'cuenta']

    def __init__(self, *args, **kwargs):
        self.orden = kwargs.pop('orden')
        super(ProductoVentaInlineForm, self).__init__(*args, **kwargs)
        existe = False
        if self.orden:
            if self.orden.cuenta:
                self.fields['producto'].queryset = inventario.Venta.objects.filter(cuenta=self.orden.cuenta, existencias__gt=0)
                existe= True
        if not existe:
            self.fields['producto'].queryset = inventario.Venta.objects.none()

    def clean(self):
        data = super(ProductoVentaInlineForm, self).clean()
        print 'este es el producto --> '
        if not data.get('producto'):
            self.add_error('producto', 'Debe seleccionar un producto.')
        if data.get('cantidad'):
            if data.get('cantidad') < 0:
                self.data('La cantidad  debe ser mayor o igual a cero')