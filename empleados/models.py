from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Empleado(models.Model):
    identificacion = models.CharField(max_length=20, unique=True)
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
