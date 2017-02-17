from __future__ import unicode_literals

from django.db import models

# Create your models here.

class TipoServicio(models.Model):
    total = models.FloatField(default=0.0, null=True, blank=True)
    comision = models.FloatField(default=0.0, null=True, blank=True) 
    inicio = models.DateField()
    fin = models.DateField()

    class Meta:
        verbose_name = 'Cierre dia tipo de servicios'
        verbose_name_plural = "Cierres de dias de tipos de servicio"
    # end class
# end class


class Factura(models.Model):
    total = models.FloatField(default=0.0, null=True, blank=True)
    comision = models.FloatField(default=0.0, null=True, blank=True)
    inicio = models.DateField()
    fin = models.DateField()

    class Meta:
        verbose_name = 'Cierre de factura'
        verbose_name_plural = "Cierres de facturas"
    # end class
# end class
