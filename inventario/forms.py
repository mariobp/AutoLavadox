# -*- coding: utf-8 -*-
from django import forms
from django.db.models import Q

import models
from autolavadox import service


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
        producto = super(ProductoVentaForm, self).save(commit)
        if self.cuenta:
            producto.cuenta=self.cuenta
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

    def clean(self):
        data = super(ProductoOperacionForm, self).clean()
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
        producto = super(ProductoOperacionForm, self).save(commit)
        if self.cuenta:
            producto.cuenta=self.cuenta
        producto.save()
        return producto


class ProductoOperacionAdminForm(forms.ModelForm):
    class Meta:
        model = models.Operacion
        fields = ['nombre', 'descripcion', 'existencias', 'stock_minimo', 'precio_compra', 'precio_venta', 'presentacion', 'cuenta']
        exclude = []

    def clean(self):
        data = super(ProductoOperacionAdminForm, self).clean()
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
