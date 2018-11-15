# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.core import validators
import re
from supra import views as supra
from django.core.validators import MaxLengthValidator
from subcripcion import models as suscripcion


# Create your models here.
class TipoVehiculo(models.Model):
    nombre = models.CharField(max_length=200, null=True, blank=True)
    descripcion = models.CharField(max_length=1000, null=True, blank=True)
    estado = models.BooleanField(default=True)
    cuenta = models.ForeignKey(suscripcion.Cuenta, null=True, blank=True)

    def __unicode__(self):
        return self.nombre if self.nombre else 'Sin asignar'
    # end def

    def __str__(self):
        return self.nombre if self.nombre else 'Sin asignar'
    # end def

    class Meta:
        verbose_name = "Tipo de Vehiculo"
        verbose_name_plural = "Tipos de vehiculo"
    # en class
# end class


class Cliente(models.Model):
    identificacion = models.CharField(max_length=20, null=True, blank=True, validators=[validators.RegexValidator(re.compile('^([1-9]+[0-9]*){7,20}$'), ('Identificacion no valida'), 'invalid')])
    nombre = models.CharField(max_length=100, null=True, blank=True)
    apellidos = models.CharField(max_length=300, null=True, blank=True)
    dirreccion = models.CharField(max_length=300, null=True, blank=True)
    correo = models.EmailField(max_length=200, verbose_name="Correo electrònico", null=True, blank=True)
    celular = models.CharField(max_length=10, validators=[validators.RegexValidator(re.compile('^([1-9]+[0-9]*){6,20}$'), ('Celular no valida'), 'invalid')], null=True, blank=True)
    nacimiento = models.DateField(verbose_name="Fecha de nacimiento", null=True, blank=True)
    cuenta = models.ForeignKey(suscripcion.Cuenta, related_name='cliente_lavado_cuenta',  null=True, blank=True)
    usuario = models.ForeignKey(User, null=True, blank=True, related_name='usuario_cliente')

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
    placa = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    marca = models.CharField(max_length=100, null=True, blank=True)
    kilometraje = models.CharField(max_length=100, null=True, blank=True)
    tipo = models.ForeignKey(TipoVehiculo, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True)

    def __unicode__(self):
        return self.placa if self.placa else 'Sin Asignar'
    # end def

    def __str__(self):
        return self.placa if self.placa else 'Sin Asignar'
    # end def

    class Meta:
        verbose_name = "Vehiculo"
        verbose_name_plural = "Vehiculos"
    # end class
# end class


class HistorialKilometraje(models.Model):
    vehiculo = models.ForeignKey(Vehiculo)
    kilometraje = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Historial de Kilometraje"
        verbose_name_plural = "Historial de Kilometraje"
    # end class
# end class
