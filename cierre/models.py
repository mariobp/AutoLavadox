# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from subcripcion import models as suscripcion
# Create your models here.

class TipoServicio(models.Model):
    total = models.FloatField(default=0.0, null=True, blank=True)
    comision = models.FloatField(default=0.0, null=True, blank=True)
    inicio = models.DateField()
    fin = models.DateField()
    cuenta = models.ForeignKey(suscripcion.Cuenta, null=True, blank=True)

    class Meta:
        verbose_name = 'Cierre dia tipo de servicios'
        verbose_name_plural = "Cierres de dias de tipos de servicio"
    # end class
# end class


class Factura(models.Model):
    total = models.FloatField(default=0.0, null=True, blank=True,verbose_name='Total factura')
    comision = models.FloatField(default=0.0, null=True, blank=True,verbose_name='Total comisión')
    inicio = models.DateField()
    fin = models.DateField()
    cuenta = models.ForeignKey(suscripcion.Cuenta, null=True, blank=True)

    class Meta:
        verbose_name = 'Cierre de factura'
        verbose_name_plural = "Cierres de facturas"
    # end class
# end class
