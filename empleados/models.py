from __future__ import unicode_literals

from django.db import models
import re
from django.core import validators
from django.contrib.auth.models import User


# Create your models
class Persona(User):
    identificacion = models.CharField(max_length=20, unique=True, validators=[validators.RegexValidator(re.compile('^([1-9]+[0-9]*){7,20}$'), ('No valida'), 'invalid')])
    direccion = models.CharField(max_length=300)
    nacimiento = models.DateField(verbose_name="Fecha de nacimiento", null=True,blank=True)
    telefono = models.CharField(max_length=10, null=True, blank=True)
    imagen = models.ImageField(upload_to="avatar", null=True, blank=True)

    def __unicode__(self):
        return '%s %s' % (self.last_name, self.first_name)
    # end def

    def __str__(self):
        return '%s %s' % (self.last_name, self.first_name)
    # end def
# end class


class Empleado(Persona):
    class Meta:
        verbose_name = "Operario"
        verbose_name_plural = "Operarios"
    # end class
# end class


class Recepcionista(Persona):
    class Meta:
        verbose_name = "Recepcionistas"
        verbose_name_plural = "Recepcionistas"
    # end class
# end class


class Cajero(Persona):
    class Meta:
        verbose_name = "Cajero"
        verbose_name_plural = "Cajeros"
    # end class
# end class
