# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from cliente import models as cliente
from empleados import models as empleado
from django.core import validators
import re
from subcripcion import models as suscripcion
from inventario import models as inventario

# Create your models here.
class TipoServicio(models.Model):
    nombre = models.CharField(max_length=500, null=True, blank=True)
    costo = models.FloatField(default=0)
    comision = models.FloatField("Comisión", default=0)
    vehiculos = models.ManyToManyField(cliente.TipoVehiculo, null=True, blank=True)
    cuenta = models.ForeignKey(suscripcion.Cuenta, related_name='tipo_ser_cuenta', null=True, blank=True)
    state = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre if self.nombre else 'Sin asignar'
    # end def

    def __str__(self):
        return self.nombre if self.nombre else 'Sin asignar'
    # end def

    class Meta:
        verbose_name = "Tipo de Servicio"
        verbose_name_plural = "Tipos de Servicio"
    # end class
# end class


class Orden(models.Model):
    entrada = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fin = models.DateTimeField(blank=True, null=True)
    recepcionista = models.ForeignKey(empleado.Recepcionista, related_name='recepcionista', null=True, blank=True)
    cajero = models.ForeignKey(empleado.Cajero, related_name='cajero', null=True, blank=True)
    vehiculo = models.ForeignKey(cliente.Vehiculo, null=True, blank=True)
    observacion = models.TextField(max_length=1000, null=True, blank=True)
    valor = models.FloatField(default=0)
    comision = models.FloatField(default=0, verbose_name="Comisión")
    cerrada = models.BooleanField(default=False)
    cancelada = models.BooleanField(default=False)
    pago = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    numero = models.IntegerField(default=0)
    cuenta = models.ForeignKey(suscripcion.Cuenta, null=True, blank=True)
    turno = models.IntegerField(default=0)

    def __unicode__(self):
        codigo = ""
        for i in range(10-len(str(self.pk))):
            codigo = codigo + "0"
        # end for
        return "#%s%d" % (codigo, self.pk)
    # end def

    def __str__(self):
        return '%s %s - %s' % (self.vehiculo.cliente.nombre, self.vehiculo.cliente.apellidos, self.vehiculo.placa)
    # end def

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
    # end class


# end class


class Servicio(models.Model):
    orden = models.ForeignKey(Orden, null=True, blank=True)
    operario = models.ManyToManyField(empleado.Empleado, blank=True)
    tipo = models.ForeignKey(TipoServicio, null=True, blank=True)
    valor = models.FloatField(default=0)
    comision = models.FloatField(verbose_name="comisión", default=0)
    estado = models.BooleanField(default=False)
    inicio = models.DateTimeField(null=True, blank=True)
    fin = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=True)
    cuenta = models.ForeignKey(suscripcion.Cuenta, null=True, blank=True)

    def __unicode__(self):
        return '%s' % (self.tipo.nombre if self.tipo else 'Sin asignar')
    # end def

    def __str__(self):
        return '%s' % (self.tipo.nombre if self.tipo else 'Sin asignar')
    # end def

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
    # en class
# end class


class ComposicionServicio(models.Model):
    servicio = models.ForeignKey(TipoServicio, null=True, blank=True)
    cuenta = models.ForeignKey(suscripcion.Cuenta, null=True, blank=True)

    def __unicode__(self):
        return self.servicio.nombre if self.servicio else 'Sin Asignar'

    def __str__(self):
        return self.servicio.nombre if self.servicio else 'Sin Asignar'

    class Meta:
        verbose_name = 'Composicion de Servicio'
        verbose_name_plural = 'Composiciones de Servicios'


class Componente(models.Model):
    composicion = models.ForeignKey(ComposicionServicio, null=True, blank=True)
    producto = models.ForeignKey(inventario.Operacion, null=True, blank=True)
    cantidad = models.FloatField(default=0)
    cuenta = models.ForeignKey(inventario.Cuenta, null=True, blank=True)

    def __unicode__(self):
        return self.producto.nombre if self.producto else 'Sin Asignar'

    def __str__(self):
        return self.producto.nombre if self.producto else 'Sin Asignar'


class ProductoVenta(models.Model):
    orden = models.ForeignKey(Orden, null=True, blank=True)
    producto = models.ForeignKey(inventario.Venta)
    cantidad = models.IntegerField(default=0)
    total = models.FloatField(default=0)
    cuenta = models.ForeignKey(suscripcion.Cuenta, null=True, blank=True)

    def __unicode__(self):
        return self.producto.nombre if self.producto else 'Seleccionar producto'

    def __str__(self):
        return self.producto.nombre if self.producto else 'Seleccionar producto'

    class Meta:
        verbose_name = 'Producto a la Venta'
        verbose_name_plural = 'Productos a la Venta'


class HistoriaDeServicioVenta(models.Model):
    orden = models.ForeignKey(Orden)
    producto = models.ForeignKey(inventario.Venta)
    cantidad = models.FloatField(default=0)
    activo = models.BooleanField(default=True)


class HistoriaDeServicioOperacion(models.Model):
    orden = models.ForeignKey(Orden)
    producto = models.ForeignKey(inventario.Operacion)
    cantidad = models.FloatField(default=0)
    activo = models.BooleanField(default=True)


