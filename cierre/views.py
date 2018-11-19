#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from autolavadox import service
from django.db.models import Q
from subcripcion import models as suscripcion

class FacturaT(PDFTemplateView):
    template_name = "cierre/factura.html"

    def get_context_data(self, **kwargs):
        factura = get_object_or_404(models.Factura, pk=kwargs['pk'])
        cursor = connection.cursor()
        ser = service.Service.get_instance()
        tem_cuenta,is_user,admin = ser.isUser()
        cliente=False
        if tem_cuenta :
            cuenta = ser.getCuenta()
            cliente = cuenta.cliente
            cursor.execute('select cierre_factura_cuenta(\'%s\',\'%s\',%d::integer)'%(factura.inicio, factura.fin,cuenta.id))
        else:
            cursor.execute('select cierre_factura(\'%s\',\'%s\')'%(factura.inicio, factura.fin))
        #end if
        row=cursor.fetchone()
        resul = row[0][0]
        print "Esto es el resul server ",resul
        print resul['existe']
        print resul['facturas'] if resul['facturas'] else []
        print resul['total'] if resul['total'] else []
        return super(FacturaT, self).get_context_data(
            pagesize="A5",fin=factura.fin,inicio=factura.inicio,
            existe=resul['existe'], f=resul['facturas'] if resul['facturas'] else [] , total=resul['total'] if resul['total'] else [],comi=resul['comi'] if resul['comi'] else [],
            cerradas=resul['cerradas'] if resul['cerradas'] else [],cliente=cliente if cliente else [],canceladas=resul['canceladas'] if resul['canceladas'] else [],totales=resul['totales'][0] if resul['totales'][0] else [],title="Reporte Dia",
            **kwargs)
# end class


class FacturaTipo(PDFTemplateView):
    template_name = "cierre/factura_tipo.html"

    def get_context_data(self, **kwargs):
        factura = get_object_or_404(models.TipoServicio, pk=kwargs['pk'])
        cursor = connection.cursor()
        ser = service.Service.get_instance()
        tem_cuenta,is_user,admin = ser.isUser()
        if tem_cuenta :
            cuenta = ser.getCuenta()
            cursor.execute('select cierre_total_tipo_factura_cuenta(\'%s\',\'%s\',%d::integer)'%(factura.inicio, factura.fin,cuenta.id))
        else:
            cursor.execute('select cierre_total_tipo_factura(\'%s\',\'%s\')'%(factura.inicio, factura.fin))
        #end if
        row=cursor.fetchone()
        resul = row[0][0]
        return super(FacturaTipo, self).get_context_data(
            pagesize="A5",fin=factura.fin,inicio=factura.inicio,existe=resul['existe'], f=resul['facturas'], total=resul['total'],comi=resul['comi'],
            title="Reporte Dia",
            **kwargs
        )
    # end def
# end class


class FacturaTurno(PDFTemplateView):
    template_name = "cierre/factura_turno.html"

    def get_context_data(self, **kwargs):
        factura = get_object_or_404(models.Cierre, pk=kwargs['pk'])
        cursor = connection.cursor()
        sql = 'select get_cierre_turno(%d,%d)' % (factura.id, factura.cuenta.id)
        cursor.execute(sql)
        # end if
        row = cursor.fetchone()
        resul = row[0][0]
        print resul
        return super(FacturaTurno, self).get_context_data(
            pagesize="A5", fin=factura.fin, inicio=factura.inicio, fac=resul['descripcion'],
            fac_res=resul['total'], pro= resul['productos'], pro_res= resul['productos_total'],
            title="Reporte Dia",
            **kwargs
        )
        # end def

