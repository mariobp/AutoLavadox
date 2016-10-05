from __future__ import unicode_literals

from django.db import models
import re
from django.core import validators


# Create your models here.
class Empleado(models.Model):
    identificacion = models.CharField(max_length=20, unique=True, validators=[validators.RegexValidator(re.compile('^([1-9]+[0-9]*){7,20}$'), ('No valida'), 'invalid')])
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=300)

    def __unicode__(self):
        return '%s %s' % (self.nombre, self.apellidos)
    # end def

    def __str__(self):
        return '%s %s' % (self.nombre, self.apellidos)
    # end def

    class Meta:
        verbose_name = "Trabajador"
        verbose_name_plural = "Trabajadores"
    # end class
# end class
