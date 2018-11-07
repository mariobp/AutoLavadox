# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from operacion.models import Servicio, TipoServicio
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
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=3000, null=True, blank=True)
    existencias = models.FloatField(default=0)
    stock_minimo = models.FloatField(default=0)
    precio_compra = models.FloatField(default=0)
    precio_venta = models.FloatField(default=0)
    presentacion = models.ForeignKey(Presentacion, null=True, blank=True)
    cuenta = models.ForeignKey(Cuenta, null=True, blank=True)

    def __unicode__(self):
        return self.nombre

    def __str__(self):
        return self.nombre

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


class ComposicionServicio(models.Model):
    servicio = models.ForeignKey(TipoServicio, null=True, blank=True)
    cuenta = models.ForeignKey(Cuenta, null=True, blank=True)

    def __unicode__(self):
        return self.servicio.nombre if self.servicio else ''

    def __str__(self):
        return self.servicio.nombre if self.servicio else ''

    class Meta:
        verbose_name = 'Composicion de Servicio'
        verbose_name_plural = 'Composiciones de Servicios'


class Componente(models.Model):
    composicion = models.ForeignKey(ComposicionServicio, null=True, blank=True)
    producto = models.ForeignKey(Operacion, null=True, blank=True)
    cantidad = models.FloatField(default=0)
    cuenta = models.ForeignKey(Cuenta, null=True, blank=True)

    def __unicode__(self):
        return self.producto.nombre if self.producto else ''

    def __str__(self):
        return self.producto.nombre if self.producto else ''
