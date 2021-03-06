from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
# Create your views here.
from django.shortcuts import render
from supra import views as supra
from cliente import models as cliente
import models
import forms
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse
from django.views.generic import TemplateView
from datetime import date, timedelta, datetime
import re
from django.utils import timezone
import csv
from django.views.generic import View
from datetime import date
import json
from django.db import connection
import xlwt
from easy_pdf.views import PDFTemplateView
from django.db import connection


class Factura(PDFTemplateView):
    template_name = "cierre/factura.html"

    def get_context_data(self, **kwargs):
        factura = get_object_or_404(models.Factura, pk=kwargs['pk'])
        cursor = connection.cursor()
        cursor.execute('select cierre_factura(\'%s\',\'%s\')'%(factura.inicio, factura.fin))
        row=cursor.fetchone()
        resul = row[0][0]
        return super(Factura, self).get_context_data(
            pagesize="A5",fin=factura.fin,inicio=factura.inicio,existe=resul['existe'], f=resul['facturas'], total=resul['total'],comi=resul['comi'],
            title="Reporte Dia",
            **kwargs
        )
    # end def
# end class


class FacturaTipo(PDFTemplateView):
    template_name = "cierre/factura_tipo.html"

    def get_context_data(self, **kwargs):
        factura = get_object_or_404(models.TipoServicio, pk=kwargs['pk'])
        cursor = connection.cursor()
        cursor.execute('select cierre_total_tipo_factura(\'%s\',\'%s\')'%(factura.inicio, factura.fin))
        row=cursor.fetchone()
        resul = row[0][0]
        return super(FacturaTipo, self).get_context_data(
            pagesize="A5",fin=factura.fin,inicio=factura.inicio,existe=resul['existe'], f=resul['facturas'], total=resul['total'],comi=resul['comi'],
            title="Reporte Dia",
            **kwargs
        )
    # end def
# end class
