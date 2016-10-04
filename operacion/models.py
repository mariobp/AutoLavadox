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


class Servicio(models.Model):
    tipo = models.ForeignKey(TipoServicio)
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    vehiculo = models.ForeignKey(cliente.Vehiculo)
    valor = models.FloatField(default=0)
    comision = models.FloatField(verbose_name="comisión", default=0)
    pago = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s %s - %s' % (self.vehiculo.cliente.nombre, self.vehiculo.cliente.apellidos, self.tipo.nombre)
    # end def

    def __str__(self):
        return '%s %s - %s' % (self.vehiculo.cliente.nombre, self.vehiculo.cliente.apellidos, self.tipo.nombre)
    # end def

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
    # en class
# end class
