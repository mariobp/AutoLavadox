# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from easy_pdf.views import PDFTemplateView
from django.db import connection
from autolavadox import service
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
import models
# Create your views here.


class CierreView(PDFTemplateView):
    template_name = "inventario/cierre_inventario.html"

    def get_context_data(self, **kwargs):
        factura = get_object_or_404(models.Cierre, pk=kwargs['pk'])
        cursor = connection.cursor()
        sql = 'select get_cierre_inventario(%d,%d)' % (factura.id, factura.cuenta.id)
        cursor.execute(sql)
        # end if
        row = cursor.fetchone()
        resul = row[0][0]
        return super(CierreView, self).get_context_data(
            pagesize="A5", fin=factura.fin, inicio=factura.inicio, venta=resul['venta'],
            venta_total=resul['venta_total'], operacion= resul['operacion'], operacion_total= resul['operacion_total'],
            title="Reporte cierre inventario",
            **kwargs
        )
        # end def

