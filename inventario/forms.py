# -*- coding: utf-8 -*-
from django import forms
from django.db.models import Q
from django.forms.models import BaseInlineFormSet, BaseModelFormSet
import models
from autolavadox import service
from easy_select2 import apply_select2, Select2Multiple
from django.contrib.admin import widgets


class PresentacionForm(forms.ModelForm):
    class Meta:
        model = models.Presentacion
        fields = ['nombre']
        exclude = ['activo']

    def __init__(self, *args, **kwargs):
        super(PresentacionForm, self).__init__(*args, **kwargs)
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if tem_cuenta and is_user:
            self.cuenta = ser.getCuenta()


    def clean(self):
        data = super(PresentacionForm, self).clean()
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
        fields = ['nombre', 'cuenta']
        exclude = [ 'activo']


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
        widgets = {
            'cuenta': apply_select2(forms.Select),
            'presentacion': apply_select2(forms.Select)
        }

    def __init__(self, *args, **kwargs):
        super(ProductoVentaForm, self).__init__(*args, **kwargs)
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if tem_cuenta and is_user:
            self.cuenta = ser.getCuenta()
            self.fields['presentacion'].queryset = self.cuenta.presentacion_set.all()

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

        if data.get('existencias'):
            if data.get('existencias') < 0:
                self.add_error('existencias', 'Las existencias deben mayores igual a cero.')

        if data.get('stock_minimo'):
            if data.get('stock_minimo') < 0:
                self.add_error('stock_minimo', 'Las stock deben mayores igual a cero.')

        if data.get('precio_compra'):
            if data.get('precio_compra') < 0:
                self.add_error('precio_compra', 'El precio de venta debe mayores igual a cero.')

        if data.get('precio_venta'):
            if data.get('precio_venta') < 0:
                self.add_error('precio_venta', 'Las stock deben mayores igual a cero.')

        if not data.get('presentacion'):
            self.add_error('presentacion', 'Debe seleccionar una presentacion.')


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
        widgets = {
            'cuenta': apply_select2(forms.Select),
            'presentacion': apply_select2(forms.Select)
        }

    def __init__(self, *args, **kwargs):
        super(ProductoVentaAdminForm, self).__init__(*args, **kwargs)
        if self.fields.has_key('presentacion'):
            self.fields['presentacion'].queryset = self.instance.cuenta.presentacion_set.all()


    def clean(self):
        data = super(ProductoVentaAdminForm, self).clean()
        productos = None
        if self.fields.has_key('presentacion'):
            if not data.get('presentacion'):self.add_error('presentacion', 'Debe selecionar una opcion.')
        if self.fields.has_key('cuenta'):
            if not data.get('cuenta'):
                self.add_error('cuenta', 'Debe asociar una cuenta.')
        if self.fields.has_key('nombre'):
            if data.get('nombre'):
                productos = self.instance.cuenta.producto_set.all()
                productos = self.instance.cuenta.producto_set.all().values_list('id', flat=True)
                productos = models.Venta.objects.filter(id__in=list(productos) if productos else [])
                if productos:
                    existir_producto = productos.filter(Q(nombre=data.get('nombre').title())&~Q(id=self.instance.id if self.instance else 0))
                    if existir_producto:
                        self.add_error('nombre', 'Existe un producto regitrado con este nombre.')
            else:
                self.add_error('nombre', 'Debe digitar el nombre.')
        if self.fields.has_key('existencia'):
            if data.get('existencias'):
                if data.get('existencias') < 0:
                    self.add_error('existencias', 'Las existencias deben mayores igual a cero.')
        if self.fields.has_key('stock_minimo'):
            if data.get('stock_minimo'):
                if data.get('stock_minimo') < 0:
                    self.add_error('stock_minimo', 'Las stock deben mayores igual a cero.')
        if self.fields.has_key('precio_compra'):
            if data.get('precio_compra'):
                if data.get('precio_compra') < 0:
                    self.add_error('precio_compra', 'El precio de venta debe mayores igual a cero.')
        if self.fields.has_key('precio_venta'):
            if data.get('precio_venta'):
                if data.get('precio_venta') < 0:
                    self.add_error('precio_venta', 'Las stock deben mayores igual a cero.')
        if self.fields.has_key('tipo'):
            if not data.get('tipo'):
                self.add_error('tipo', 'Debe seleccionar un Tipo.')

    def save(self, commit=True):
        venta = super(ProductoVentaAdminForm, self).save(commit)
        if self.fields.has_key('nombre'):
            venta.nombre = venta.nombre.title() if venta.nombre else ''
            venta.save()
        return venta


class ProductoOperacionForm(forms.ModelForm):

    class Meta:
        model = models.Operacion
        fields = ['nombre', 'descripcion', 'existencias', 'stock_minimo', 'precio_compra', 'precio_venta', 'presentacion']
        exclude = ['cuenta']
        widgets = {
            'cuenta': apply_select2(forms.Select),
            'presentacion': apply_select2(forms.Select)
        }

    def __init__(self, *args, **kwargs):
        super(ProductoOperacionForm, self).__init__(*args, **kwargs)
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if tem_cuenta and is_user:
            self.cuenta = ser.getCuenta()
            self.fields['presentacion'].queryset = self.cuenta.presentacion_set.all()
        self.fields['precio_venta'].label = 'Precio de operacion'

    def clean(self):
        data = super(ProductoOperacionForm, self).clean()
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

        if data.get('existencias'):
            if data.get('existencias') < 0:
                self.add_error('existencias', 'Las existencias deben mayores igual a cero.')

        if data.get('stock_minimo'):
            if data.get('stock_minimo') < 0:
                self.add_error('stock_minimo', 'Las stock deben mayores igual a cero.')

        if data.get('precio_compra'):
            if data.get('precio_compra') < 0:
                self.add_error('precio_compra', 'El precio de venta debe mayores igual a cero.')

        if data.get('precio_venta'):
            if data.get('precio_venta') < 0:
                self.add_error('precio_venta', 'Las stock deben mayores igual a cero.')

        if not data.get('presentacion'):
            self.add_error('presentacion', 'Debe seleccionar una presentacion.')

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
        widgets = {
            'cuenta': apply_select2(forms.Select),
            'presentacion': apply_select2(forms.Select)
        }

    def __init__(self, *args, **kwargs):
        super(ProductoOperacionAdminForm, self).__init__(*args, **kwargs)
        if  self.fields.has_key('precio_venta'):
            self.fields['precio_venta'].label = 'Precio de operacion'
        if self.fields.has_key('presentacion'):
            self.fields['presentacion'].queryset = self.instance.cuenta.presentacion_set.all()

    def clean(self):
        data = super(ProductoOperacionAdminForm, self).clean()
        productos = None
        if self.fields.has_key('presentacion'):
            if not data.get('presentacion'): self.add_error('presentacion', 'Debe selecionar una opcion.')
        if self.fields.has_key('cuenta'):
            if not data.get('cuenta'):
                self.add_error('cuenta', 'Debe asociar una cuenta.')
        if self.fields.has_key('nombre'):
            if data.get('nombre'):
                productos = self.instance.cuenta.producto_set.all()
                productos = self.instance.cuenta.producto_set.all().values_list('id', flat=True)
                productos = models.Venta.objects.filter(id__in=list(productos) if productos else [])
                if productos:
                    existir_producto = productos.filter(
                        Q(nombre=data.get('nombre').title()) & ~Q(id=self.instance.id if self.instance else 0))
                    if existir_producto:
                        self.add_error('nombre', 'Existe un producto regitrado con este nombre.')
            else:
                self.add_error('nombre', 'Debe digitar el nombre.')
        if self.fields.has_key('existencia'):
            if data.get('existencias'):
                if data.get('existencias') < 0:
                    self.add_error('existencias', 'Las existencias deben mayores igual a cero.')
        if self.fields.has_key('stock_minimo'):
            if data.get('stock_minimo'):
                if data.get('stock_minimo') < 0:
                    self.add_error('stock_minimo', 'Las stock deben mayores igual a cero.')
        if self.fields.has_key('precio_compra'):
            if data.get('precio_compra'):
                if data.get('precio_compra') < 0:
                    self.add_error('precio_compra', 'El precio de venta debe mayores igual a cero.')
        if self.fields.has_key('precio_venta'):
            if data.get('precio_venta'):
                if data.get('precio_venta') < 0:
                    self.add_error('precio_venta', 'Las stock deben mayores igual a cero.')
        if self.fields.has_key('tipo'):
            if not data.get('tipo'):
                self.add_error('tipo', 'Debe seleccionar un Tipo.')

    def save(self, commit=True):
        producto = super(ProductoOperacionAdminForm, self).save(commit)
        if producto.nombre:
            producto.nombre = producto.nombre.title()
        producto.save()
        return producto


class CierreadminForm(forms.ModelForm):
    class Meta:
        model = models.Cierre
        fields = ['cuenta', 'inicio', 'fin', 'costo_producto_venta', 'utilidad_producto_venta', 'total_producto_venta', 'costo_producto_operacion', 'utilidad_producto_operacion', 'total_producto_operacion']
        widgets = {
            'tipo': apply_select2(forms.Select),
        }

    def __init__(self, *args, **kwargs):
        super(CierreadminForm, self).__init__(*args, **kwargs)
        if self.fields.has_key('inicio'):
            self.fields['inicio'].widget = widgets.AdminDateWidget()
        if self.fields.has_key('fin'):
            self.fields['fin'].widget = widgets.AdminDateWidget()

    def clean(self):
        data = super(CierreadminForm, self).clean()
        if self.fields.has_key('cuenta'):
            if not data.get('cuenta'):
                self.add_error('cuenta', 'Debe seleccionar una cuenta')

        if self.fields.has_key('inicio'):
            if not data.get('inicio'):
                self.add_error('inicio', 'Debe digitar una fecha de inicio.')

        if self.fields.has_key('fin'):
            if not data.get('fin'):
                self.add_error('fin', 'Debe digitar una fecha de fin.')
        if self.fields.has_key('inicio') and self.fields.has_key('fin'):
            if data.get('inicio') and data.get('fin'):
                if data.get('inicio') > data.get('fin'):
                    self.add_error('inicio', 'La fecha de inicio debe ser mayor a la inicial.')


class CierreForm(forms.ModelForm):
    class Meta:
        model = models.Cierre
        fields = ['inicio', 'fin', 'costo_producto_venta', 'utilidad_producto_venta', 'total_producto_venta', 'costo_producto_operacion', 'utilidad_producto_operacion', 'total_producto_operacion']
        widgets = {
            'tipo': apply_select2(forms.Select),
        }

    def __init__(self, *args, **kwargs):
        super(CierreForm, self).__init__(*args, **kwargs)
        self.fields['inicio'].widget = widgets.AdminDateWidget()
        self.fields['fin'].widget = widgets.AdminDateWidget()
        ser = service.Service.get_instance()
        self.cuenta = ser.getCuenta()

    def clean(self):
        data = super(CierreForm, self).clean()
        if self.fields.has_key('cuenta'):
            if not data.get('cuenta'):
                self.add_error('cuenta', 'Debe seleccionar una cuenta')

        if self.fields.has_key('inicio'):
            if not data.get('inicio'):
                self.add_error('inicio', 'Debe digitar una fecha de inicio.')

        if self.fields.has_key('fin'):
            if not data.get('fin'):
                self.add_error('fin', 'Debe digitar una fecha de fin.')
        if self.fields.has_key('inicio') and self.fields.has_key('fin'):
            if data.get('inicio') and data.get('fin'):
                if data.get('inicio') > data.get('fin'):
                    self.add_error('inicio', 'La fecha de inicio debe ser mayor a la inicial.')

    def save(self, commit=True):
        producto = super(CierreForm, self).save(commit)
        if self.cuenta:
            producto.cuenta=self.cuenta
        producto.save()
        return producto