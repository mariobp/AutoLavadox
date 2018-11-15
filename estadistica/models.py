from __future__ import unicode_literals
from operacion import models as operacion
from django.db import models
from subcripcion import models as suscripcion


class TiemposOrden(models.Model):
    orden = models.ForeignKey(operacion.Orden)
    inicio = models.DateField()
    fin = models.DateField()
    cuenta = models.ForeignKey(suscripcion.Cuenta, related_name='tiempo_cuenta', null=True, blank=True)

    def __unicode__(self):
        return '%s' % (self.orden.vehiculo.placa)
    # end def

    def __str__(self):
        return '%s' % (self.orden.vehiculo.placa)
    # end def

    class Meta:
        verbose_name = "Tiempos de orden"
        verbose_name_plural = "Tiempos de ordenes"
    # end class
# end class
