# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from cliente import models as cliente
from empleados import models as empleado


# Create your models here.
class TipoServicio(models.Model):
    nombre = models.CharField(max_length=500, unique=True)
    costo = models.FloatField()
    comision = models.FloatField("Comisión")
    state = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre
    # end def

    def __str__(self):
        return self.nombre
    # end def

    class Meta:
        verbose_name = "Tipo de Servicio"
        verbose_name_plural = "Tipos de Servicio"
    # end class
# end class


class Orden(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    entrega = models.DateField(auto_now_add=True, blank=True, null=True)
    vehiculo = models.ForeignKey(cliente.Vehiculo, null=True, blank=True)
    observacion = models.CharField(max_length=1000, null=True, blank=True)
    valor = models.FloatField(default=0)
    comision = models.FloatField(default=0, verbose_name="Comisión")
    pago = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s %s - %s' % (self.vehiculo.cliente.nombre, self.vehiculo.cliente.apellidos, self.vehiculo.placa)
    # end def

    def __str__(self):
        return '%s %s - %s' % (self.vehiculo.cliente.nombre, self.vehiculo.cliente.apellidos, self.vehiculo.placa)
    # end def

    class Meta:
        verbose_name = "Orden"
        verbose_name_plural = "Ordenes"
    # end class
# end class


class Servicio(models.Model):
    orden = models.ForeignKey(Orden, null=True, blank=True)
    empleado = models.ForeignKey(empleado.Empleado)
    tipo = models.ForeignKey(TipoServicio)
    valor = models.FloatField(default=0)
    comision = models.FloatField(verbose_name="comisión", default=0)
    estado = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s' % (self.tipo.nombre)
    # end def

    def __str__(self):
        return '%s' % (self.tipo.nombre)
    # end def

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
    # en class
# end class
