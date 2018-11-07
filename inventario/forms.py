# -*- coding: utf-8 -*-
from django import forms
from django.db.models import Q
from django.forms.models import BaseInlineFormSet, BaseModelFormSet
import models
from autolavadox import service
from operacion.models import TipoServicio


class PresentacionForm(forms.ModelForm):
    class Meta:
        model = models.Presentacion
        fields = ['nombre', 'activo']
        exclude = []

    def __init__(self, *args, **kwargs):
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if tem_cuenta and is_user:
            self.cuenta = ser.getCuenta()


    def clean(self):
        data = super(PresentacionAdminForm, self).clean()
        if data.get('nombre'):
            presentacion = models.Presentacion.objects.filter(Q(nombre=data.get('nombre').title(), cuenta=self.cuenta)&~Q(id= self.instance.id if self.instance else 0)).first()
            if presentacion:
                self.add_error('nombre', 'El nombre se encuentra registrado.')


    def save(self, commit=True):
        presentacion = super(PresentacionForm, self).save(commit)
        presentacion.nombre = presentacion.nombre.title()
        presentacion.cuenta = self.cuenta
        presentacion.save()
        return presentacion


class PresentacionAdminForm(forms.ModelForm):
    class Meta:
        model = models.Presentacion
        fields = ['nombre', 'activo', 'cuenta']
        exclude = []


class ProductoForm(forms.ModelForm):

    class Meta:
        model = models.Producto
        fields = ['nombre', 'descripcion', 'existencias', 'stock_minimo', 'precio_compra', 'precio_venta', 'presentacion']
        exclude = ['cuenta']

    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if tem_cuenta and is_user:
            self.cuenta = ser.getCuenta()

    def clean(self):
        data = super(ProductoForm, self).clean()
        productos = None
        if self.cuenta:
            productos = self.cuenta.producto_set.all()

        if data.get('nombre'):
            if productos:
                existir_producto = productos.filter(
                    Q(nombre=data.get('nombre').title()) & ~Q(id=self.instance.id if self.instance else 0))
                if existir_producto:
                    self.add_error('nombre', 'Existe un producto regitrado con este nombre.')

        if data.get('existencia'):
            if data.get('existencia') < 0:
                self.add_error('existencia', 'Las existencias deben mayores igual a cero.')

        if data.get('stock_minimo'):
            if data.get('stock_minimo') < 0:
                self.add_error('stock_minimo', 'Las stock deben mayores igual a cero.')

        if data.get('precio_compra'):
            if data.get('precio_compra') < 0:
                self.add_error('precio_compra', 'El precio de venta debe mayores igual a cero.')

        if data.get('precio_venta'):
            if data.get('precio_venta') < 0:
                self.add_error('stock_minimo', 'Las stock deben mayores igual a cero.')

    def save(self, commit=True):
        producto = super(ProductoForm, self).save(commit)
        if self.cuenta:
            producto.cuenta=self.cuenta
        producto.nombre = producto.nombre.title()
        producto.save()
        return producto


class ProductoAdminForm(forms.ModelForm):
    class Meta:
        model = models.Producto
        fields = ['nombre', 'descripcion', 'existencias', 'stock_minimo', 'precio_compra', 'precio_venta', 'presentacion', 'cuenta']
        exclude = []

    def clean(self):
        data = super(ProductoAdminForm, self).clean()
        productos = None
        if not data.get('cuenta'):
            self.add_error('cuenta', 'Debe asociar una cuenta.')

        if data.get('cuenta'):
            productos = data.get('cuenta').producto_set.all()

        if data.get('nombre'):
            if productos:
                existir_producto = productos.filter(Q(nombre=data.get('nombre').title())&~Q(id=self.instance.id if self.instance else 0))
                if existir_producto:
                    self.add_error('nombre', 'Existe un producto regitrado con este nombre.')
        if data.get('existencia'):
            if data.get('existencia') < 0:
                self.add_error('existencia', 'Las existencias deben mayores igual a cero.')

        if data.get('stock_minimo'):
            if data.get('stock_minimo') < 0:
                self.add_error('stock_minimo', 'Las stock deben mayores igual a cero.')

        if data.get('precio_compra'):
            if data.get('precio_compra') < 0:
                self.add_error('precio_compra', 'El precio de venta debe mayores igual a cero.')

        if data.get('precio_venta'):
            if data.get('precio_venta') < 0:
                self.add_error('precio_venta', 'Las stock deben mayores igual a cero.')

    def save(self, commit=True):
        producto = super(ProductoAdminForm, self).save(commit)
        producto.nombre = producto.nombre.title()
        producto.save()
        return producto


class ProductoVentaForm(forms.ModelForm):

    class Meta:
        model = models.Venta
        fields = ['nombre', 'descripcion', 'existencias', 'stock_minimo', 'precio_compra', 'precio_venta', 'presentacion']
        exclude = ['cuenta']

    def __init__(self, *args, **kwargs):
        super(ProductoVentaForm, self).__init__(*args, **kwargs)
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if tem_cuenta and is_user:
            self.cuenta = ser.getCuenta()

    def clean(self):
        data = super(ProductoVentaForm, self).clean()
        productos = None
        if self.cuenta:
            productos = self.cuenta.producto_set.all().values_list('id', flat=True)
            productos = models.Venta.objects.filter(id__in=list(productos) if productos else [])

        if data.get('nombre'):
            if productos:
                existir_producto = productos.filter(
                    Q(nombre=data.get('nombre').title()) & ~Q(id=self.instance.id if self.instance else 0))
                if existir_producto:
                    self.add_error('nombre', 'Existe un producto regitrado con este nombre.')

        if data.get('existencia'):
            if data.get('existencia') < 0:
                self.add_error('existencia', 'Las existencias deben mayores igual a cero.')

        if data.get('stock_minimo'):
            if data.get('stock_minimo') < 0:
                self.add_error('stock_minimo', 'Las stock deben mayores igual a cero.')

        if data.get('precio_compra'):
            if data.get('precio_compra') < 0:
                self.add_error('precio_compra', 'El precio de venta debe mayores igual a cero.')

        if data.get('precio_venta'):
            if data.get('precio_venta') < 0:
                self.add_error('stock_minimo', 'Las stock deben mayores igual a cero.')

    def save(self, commit=True):
        producto = super(ProductoVentaForm, self).save(commit)
        if self.cuenta:
            producto.cuenta=self.cuenta
        producto.nombre = producto.nombre.title()
        producto.save()
        return producto


class ProductoVentaAdminForm(forms.ModelForm):
    class Meta:
        model = models.Venta
        fields = ['nombre', 'descripcion', 'existencias', 'stock_minimo', 'precio_compra', 'precio_venta', 'presentacion', 'cuenta']
        exclude = []

    def clean(self):
        data = super(ProductoVentaAdminForm, self).clean()
        productos = None
        if not data.get('cuenta'):
            self.add_error('cuenta', 'Debe asociar una cuenta.')

        if data.get('cuenta'):
            productos = data.get('cuenta').producto_set.all()
            productos = data.get('cuenta').producto_set.all().values_list('id', flat=True)
            productos = models.Venta.objects.filter(id__in=list(productos) if productos else [])

        if data.get('nombre'):
            if productos:
                existir_producto = productos.filter(Q(nombre=data.get('nombre').title())&~Q(id=self.instance.id if self.instance else 0))
                if existir_producto:
                    self.add_error('nombre', 'Existe un producto regitrado con este nombre.')
        if data.get('existencia'):
            if data.get('existencia') < 0:
                self.add_error('existencia', 'Las existencias deben mayores igual a cero.')

        if data.get('stock_minimo'):
            if data.get('stock_minimo') < 0:
                self.add_error('stock_minimo', 'Las stock deben mayores igual a cero.')

        if data.get('precio_compra'):
            if data.get('precio_compra') < 0:
                self.add_error('precio_compra', 'El precio de venta debe mayores igual a cero.')

        if data.get('precio_venta'):
            if data.get('precio_venta') < 0:
                self.add_error('precio_venta', 'Las stock deben mayores igual a cero.')

    def save(self, commit=True):
        venta = super(ProductoVentaAdminForm, self).save(commit)
        venta.nombre = venta.nombre.title()
        venta.save()
        return venta()


class ProductoOperacionForm(forms.ModelForm):

    class Meta:
        model = models.Operacion
        fields = ['nombre', 'descripcion', 'existencias', 'stock_minimo', 'precio_compra', 'precio_venta', 'presentacion']
        exclude = ['cuenta']

    def __init__(self, *args, **kwargs):
        super(ProductoOperacionForm, self).__init__(*args, **kwargs)
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if tem_cuenta and is_user:
            self.cuenta = ser.getCuenta()
        self.fields['precio_venta'].label = 'Precio de operacion'

    def clean(self):
        data = super(ProductoOperacionForm, self).clean()
        productos = None
        if self.cuenta:
            productos = self.cuenta.producto_set.all().values_list('id', flat=True)
            productos = models.Operacion.objects.filter(id__in=list(productos) if productos else [])

        if data.get('nombre'):
            if productos:
                existir_producto = productos.filter(
                    Q(nombre=data.get('nombre').title()) & ~Q(id=self.instance.id if self.instance else 0))
                if existir_producto:
                    self.add_error('nombre', 'Existe un producto regitrado con este nombre.')

        if data.get('existencia'):
            if data.get('existencia') < 0:
                self.add_error('existencia', 'Las existencias deben mayores igual a cero.')

        if data.get('stock_minimo'):
            if data.get('stock_minimo') < 0:
                self.add_error('stock_minimo', 'Las stock deben mayores igual a cero.')

        if data.get('precio_compra'):
            if data.get('precio_compra') < 0:
                self.add_error('precio_compra', 'El precio de venta debe mayores igual a cero.')

        if data.get('precio_venta'):
            if data.get('precio_venta') < 0:
                self.add_error('stock_minimo', 'Las stock deben mayores igual a cero.')

    def save(self, commit=True):
        producto = super(ProductoOperacionForm, self).save(commit)
        if self.cuenta:
            producto.cuenta=self.cuenta
        producto.nombre = producto.nombre.title()
        producto.save()
        return producto


class ProductoOperacionAdminForm(forms.ModelForm):
    class Meta:
        model = models.Operacion
        fields = ['nombre', 'descripcion', 'existencias', 'stock_minimo', 'precio_compra', 'precio_venta', 'presentacion', 'cuenta']
        exclude = []

    def __init__(self, *args, **kwargs):
        super(ProductoOperacionAdminForm, self).__init__(*args, **kwargs)
        self.fields['precio_venta'].label = 'Precio de operacion'

    def clean(self):
        data = super(ProductoOperacionAdminForm, self).clean()
        productos = None
        if not data.get('cuenta'):
            self.add_error('cuenta', 'Debe asociar una cuenta.')

        if data.get('cuenta'):
            productos = data.get('cuenta').producto_set.all().values_list('id', flat=True)
            productos = models.Operacion.objects.filter(id__in=list(productos) if productos else [])

        if data.get('nombre'):
            if productos:
                existir_producto = productos.filter(Q(nombre=data.get('nombre').title())&~Q(id=self.instance.id if self.instance else 0))
                if existir_producto:
                    self.add_error('nombre', 'Existe un producto regitrado con este nombre.')
        if data.get('existencia'):
            if data.get('existencia') < 0:
                self.add_error('existencia', 'Las existencias deben mayores igual a cero.')

        if data.get('stock_minimo'):
            if data.get('stock_minimo') < 0:
                self.add_error('stock_minimo', 'Las stock deben mayores igual a cero.')

        if data.get('precio_compra'):
            if data.get('precio_compra') < 0:
                self.add_error('precio_compra', 'El precio de venta debe mayores igual a cero.')

        if data.get('precio_venta'):
            if data.get('precio_venta') < 0:
                self.add_error('precio_venta', 'Las stock deben mayores igual a cero.')

    def save(self, commit=True):
        producto = super(ProductoOperacionAdminForm, self).save(commit)
        producto.nombre = producto.nombre.title()
        producto.save()
        return producto


class ComposicionServicioForm(forms.ModelForm):
    class Meta:
        model = models.ComposicionServicio
        fields = ['servicio']
        exclude = ['cuenta']

    def __init__(self, *args, **kwargs):
        super(ComposicionServicioForm, self).__init__(*args, **kwargs)
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        self.cuenta = ser.getCuenta()
        if not admin and self.fields.has_key('servicio'):
            self.fields['servicio'].queryset = TipoServicio.objects.filter(Q(composicionservicio__isnull=True, cuenta=self.cuenta)|Q(id=self.instance.servicio.id if self.instance.servicio else 0))

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

    def __init__(self, *args, **kwargs):
        super(ComposicionServicioAdminForm, self).__init__(*args, **kwargs)
        if self.fields.has_key('servicio') and self.instance.cuenta:
            self.fields['servicio'].queryset = TipoServicio.objects.filter(Q(composicionservicio__isnull=True, cuenta=self.instance.cuenta)|Q(id=self.instance.servicio.id if self.instance.servicio else 0))

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
                self.fields['producto'].queryset = models.Operacion.objects.filter(cuenta=self.composicion_servicio.cuenta)
                switch=True
        if not switch:
            self.fields['producto'].queryset = models.Operacion.objects.none()

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
            self.fields['producto'].queryset = models.Operacion.objects.filter(cuenta=self.cuenta)
            self.fields['composicion'].queryset = self.cuenta.composicionservicio_set.all()
        else:
            self.fields['producto'].queryset = models.Operacion.objects.none()
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
        if self.instance.cuenta:
            if self.fields.has_key('productos'):
                self.fields['productos'].queryset = models.Operacion.objects.filter(cuenta=self.instance.cuenta)
            if self.fields.has_key('composicion'):
                self.fields['composicion'].queryset = self.instance.cuenta.composicionservicio_set.all()
        else:
            if self.fields.has_key('productos'):
                self.fields['productos'].queryset = models.Operacion.objects.none()
            if self.fields.has_key('composicion'):
                self.fields['composicion'].queryset = models.ComposicionServicio.objects.none()

    def clean(self):
        data = super(ComponenteAdminForm, self).clean()
        if data.get('cantidad'):
            if data.get('cantidad') < 0:
                self.add_error('cantidad', 'La cantidad debe ser mayor a cero.')
        if not data.get('producto'):
            self.add_error('producto', 'Debe seleccionar un prodicto.')
        if not data.get('composicion'):
            self.add_error('composicion', 'Debe seleccionar una composicion')