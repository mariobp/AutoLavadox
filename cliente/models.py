from __future__ import unicode_literals

from django.db import models
from django.core import validators
import re


# Create your models here.
class TipoVehiculo(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.CharField(max_length=1000)
    estado = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre
    # end def

    def __str__(self):
        return self.nombre
    # end def

    class Meta:
        verbose_name = "Tipo de Vehiculo"
        verbose_name_plural = "Tipos de vehiculo"
    # en class
# end class


class Cliente(models.Model):
    identificacion = models.CharField(max_length=20, unique=True, validators=[validators.RegexValidator(re.compile('^([1-9]+[0-9]*){7,20}$'), ('Identificacion no valida'), 'invalid')])
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=300)

    def __unicode__(self):
        return '%s %s' % (self.nombre, self.apellidos)
    # end def

    def __str__(self):
        return '%s %s' % (self.nombre, self.apellidos)
    # end def

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
    # end class
# end class


class Vehiculo(models.Model):
    placa = models.CharField(max_length=10, unique=True)
    tipo = models.ForeignKey(TipoVehiculo)
    cliente = models.ForeignKey(Cliente)

    def __unicode__(self):
        return self.placa
    # end def

    def __str__(self):
        return self.placa
    # end def

    class Meta:
        verbose_name = "Vehiculo"
        verbose_name_plural = "Vehiculos"
    # end class
# end class
