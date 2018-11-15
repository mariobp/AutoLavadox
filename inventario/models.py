# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from subcripcion.models import Cuenta


class Presentacion(models.Model):
    nombre = models.CharField(max_length=200)
    activo = models.BooleanField(default=True)
    cuenta = models.ForeignKey(Cuenta, null=True, blank=True)

    class Meta:
        verbose_name = 'Presentacion'
        verbose_name_plural = 'Presentaciones'
        unique_together = ('nombre', 'cuenta')

    def __unicode__(self):
        return self.nombre

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=200, null=True)
    descripcion = models.TextField(max_length=3000, null=True, blank=True)
    existencias = models.FloatField(default=0)
    stock_minimo = models.FloatField(default=0)
    precio_compra = models.FloatField(default=0)
    precio_venta = models.FloatField(default=0)
    presentacion = models.ForeignKey(Presentacion, null=True, blank=True)
    cuenta = models.ForeignKey(Cuenta, null=True, blank=True)

    def __unicode__(self):
        return self.nombre if self.nombre else 'Sin asignar'

    def __str__(self):
        return self.nombre if self.nombre else 'Sin asignar'

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'


class Venta(Producto):
    class Meta:
        verbose_name = 'Producto de venta'
        verbose_name_plural = 'Productos de venta'


class Operacion(Producto):
    class Meta:
        verbose_name = 'Producto de operacion'
        verbose_name_plural = 'Productos de operacion'


class Cierre(models.Model):
    cuenta = models.ForeignKey(Cuenta, null=True, blank=True, related_name='inventario_cierre')
    inicio = models.DateField(null=True, blank=True)
    fin = models.DateField(null=True, blank=True)
    costo_producto_venta = models.FloatField(default=0, verbose_name='Costo de venta')
    utilidad_producto_venta = models.FloatField(default=0, verbose_name='Utilidad de venta')
    total_producto_venta = models.FloatField(default=0, verbose_name='Total de venta')
    costo_producto_operacion = models.FloatField(default=0, verbose_name='Costo de operacion')
    utilidad_producto_operacion = models.FloatField(default=0, verbose_name='Utilidad de operacion')
    total_producto_operacion = models.FloatField(default=0, verbose_name='Total de operacion')

    def __unicode__(self):
        size = 8 - len('{}'.format(self.id))
        info = ''
        for i in range(1, size + 1) :
            info = '{}{}'.format('0', info)
        return '{}{}'.format(info, self.id)

    def __str__(self):
        size = 8 - len('{}'.format(self.id))
        info = ''
        for i in range(1, size + 1) :
            info = '{}{}'.format('0', info)
        return '{}{}'.format(info, self.id)

    class Meta:
        verbose_name = 'Cierre de Inventario'
        verbose_name_plural = 'Cierres de Inventario'

