# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import re
from django.core import validators
# Create your models here.


class Cliente(User):
    identificacion = models.CharField(max_length=100, validators=[validators.RegexValidator(re.compile('^([1-9]+[0-9]*){7,20}$'), ('Identificacion invalida'), 'invalid')])
    direccion = models.CharField(
        "Dirección", max_length=200, blank=True, null=True)
    telefono = models.CharField(
        "Teléfono", max_length=15, blank=True, null=True)
    nombre_negocio = models.CharField(max_length=150, null=True,blank=True, verbose_name='Nombre de la empresa')
    invima = models.CharField(max_length=100, verbose_name='Registro sanitario', null=True, blank=True)
    nit = models.CharField(max_length=150, verbose_name='Nit', null=True, blank=True)
    consecutivo= models.IntegerField(default=0)
    logo = models.ImageField(upload_to = 'media/logos/', null=True, blank=True)
    impresora = models.CharField(max_length=20, blank=True, null=True, verbose_name="Nombre de la impresora")
    reiniciar = models.BooleanField(default=False, verbose_name="Reiniciar serial")
    inventario = models.BooleanField(default=False)
    ventas_sin_existencias = models.BooleanField(default=False, verbose_name='Ventas sin existencias para la operacion')
    turnero = models.IntegerField(default=0, verbose_name='Contador Turnero')
    mostrar_turno = models.BooleanField(default=True, verbose_name='Mostrar turno')

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
    # end class

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)
    # end def

    def __str__(self):
        return u'%s %s' % (self.first_name, self.last_name)
    # end def
# end class


class Plan(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=800, null=True, blank=True)
    operadores = models.IntegerField(verbose_name='Número de operadores',default=0)
    cajeros = models.IntegerField(verbose_name='Número de cajeros',default=0)
    recepcionistas = models.IntegerField(verbose_name='Número de recepcionistas',default=0)
    operario = models.BooleanField(default=True, verbose_name='App empleados')
    gerente = models.BooleanField(default=True, verbose_name='App gerente')
    duracion = models.IntegerField(verbose_name='Dias de duración en meses',default=0)
    valor = models.FloatField(default=0)
    estado = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' % (self.nombre)
    # end def

    def __str__(self):
        return u'%s' % (self.nombre)
    # end def

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Planes"
    # end class
# end class


class Cuenta(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='cliente_cuenta')
    estado = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s %s' % (self.cliente.first_name,self.cliente.last_name)
    # end def

    def __str__(self):
        return u'%s %s' % (self.cliente.first_name,self.cliente.last_name)
    # end def

    class Meta:
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"
    # end class
# end class


class Suscripcion(models.Model):
    plan = models.ForeignKey(Plan)
    cuenta = models.ForeignKey(Cuenta, null=True, blank=True)
    inscripcion = models.DateTimeField(auto_now_add=True, verbose_name='Inscripción',blank=True, null=True)
    inicio = models.DateField(blank=True, null=True)
    fin = models.DateField(blank=True, null=True)
    activa = models.BooleanField(default=True)

    def __unicode__(self):
        if self.cuenta :
            return u'%s --> %s %s' % (self.plan.nombre,self.cuenta.cliente.first_name,self.cuenta.cliente.last_name)
        # end if
        return u'%s --> No asignado.' % (self.plan.nombre)
    # end def

    def __str__(self):
        if self.cuenta :
            return u'%s --> %s %s' % (self.plan.nombre,self.cuenta.cliente.first_name,self.cuenta.cliente.last_name)
        # end if
        return u'%s --> No asignado.' % (self.plan.nombre)
    # end def

    class Meta:
        verbose_name = "Suscripción"
        verbose_name_plural = "Suscripciones"
    # end class
#end class
