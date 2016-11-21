#!/usr/bin/env python
# -*- coding: utf-8 -*-
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


class TiposServicios(supra.SupraListView):
    model = models.TipoServicio
    list_display = ['id', 'nombre', 'costo']
    search_key = 'q'
    list_filter = ['vehiculos__id']
    search_fields = ['vehiculos__id']
    paginate_by = 1000

    class Renderer:
        valor = 'costo'
    # end class

    def get_queryset(self):
        queryset = super(TiposServicios, self).get_queryset()
        obj = queryset.order_by('nombre')
        return obj
    # end def
# end class


class TiposServiciosPorAplicar(supra.SupraListView):
    model = models.TipoServicio
    list_display = ['id', 'nombre', 'valor']
    paginate_by = 1000

    class Renderer:
        valor = 'costo'
    # end class

    def get_queryset(self):
        tipo = self.request.GET.get('tipo', False)
        orden = self.request.GET.get('orden', False)
        queryset = super(TiposServiciosPorAplicar, self).get_queryset()
        obj = queryset
        oper_ser = models.Servicio.objects.filter(orden__id=int(orden) if orden and re.match('^\d+$', orden) else 0, status=True).values_list('tipo__id', flat=True)
        return queryset.filter(vehiculos__id=int(tipo) if tipo and re.match('^\d+$', tipo) else 0).exclude(id__in=list(oper_ser)).order_by('nombre')
    # end def
# end class


class AddOrdenForm(supra.SupraFormView):
    model = models.Orden
    form_class = forms.AddOrdenForm
    template_name = 'operacion/addorden.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(AddOrdenForm, self).dispatch(*args, **kwargs)
    # end def
# end class


class CancelarOrden(supra.SupraFormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CancelarOrden, self).dispatch(*args, **kwargs)
    # end def

    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        if re.match('^\d+$', id):
            orden = models.Orden.objects.filter(id=int(id)).first()
            if orden:
                orden.fin = timezone.now()
                orden.cerrada = True
                orden.cancelada = True
                # end if
                orden.save()
                return HttpResponse('{"info":"Ok"}', content_type='application/json', status=200)
            # end if
        # end if
        return HttpResponse('{"info":"Not"}', content_type='application/json', status=204)
    # end def
#end class


class CloseOrden(supra.SupraFormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CloseOrden, self).dispatch(*args, **kwargs)
    # end def

    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        if re.match('^\d+$', id):
            observacion = self.request.GET.get('observacion', False)
            orden = models.Orden.objects.filter(id=int(id)).first()
            if orden:
                orden.fin = timezone.now()
                orden.cerrada = True
                if observacion:
                    orden.observacion = observacion
                # end if
                orden.save()
                return HttpResponse('{"info":"Ok"}', content_type='application/json', status=200)
            # end if
        # end if
        return HttpResponse('{"info":"Not"}', content_type='application/json', status=204)
    # end def

    def post(self, request, *args, **kwargs):
        id = kwargs['pk']
        if re.match('^\d+$', id):
            orden = models.Orden.objects.filter(id=int(id)).first()
            if orden:
                orden.fin = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
                orden.pago = True
                orden.save()
                return HttpResponse('{"info":"Ok"}', content_type='application/json', status=200)
            # end if
        # end if
        return HttpResponse('{"info":"Not"}', content_type='application/json', status=204)
    # end def
# end class


class WsServiciosOrden(supra.SupraListView):
    model = models.Servicio
    search_key = 'q'
    list_display = ['id', 'costo', 'nombre', 'estado', 'operario', 'tipo', 'status', 'operario_nombre']
    list_filter = ['orden__id']
    search_fields = ['orden__id']
    paginate_by = 1000

    class Renderer:
        nombre = 'tipo__nombre'
        costo = 'tipo__costo'
        operario_n = "operario__first_name"
        operario_a = "operario__last_name"
    # end class

    def checked(self, obj, row):
        return True
    # end def

    def operario_nombre(self, obj, row):
        return u'%s %s' % (obj.operario_n, obj.operario_a)
    # end def

    def get_queryset(self):
        queryset = super(WsServiciosOrden, self).get_queryset()
        obj = queryset.filter(status=True)
        return obj.order_by('tipo__nombre')
    # end def
# end class


class AddServicio(supra.SupraFormView):
    model = models.Servicio
    form_class = forms.AddServicioForm
    template_name = 'operacion/addservicio.html'
    body = True

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(AddServicio, self).dispatch(*args, **kwargs)
    # end def
# end class


class OkService(supra.SupraFormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(OkService, self).dispatch(*args, **kwargs)
    # end def

    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        if re.match('^\d+$', id):
            servicio = models.Servicio.objects.filter(id=int(id)).first()
            if servicio:
                if servicio.status:
                    tem_o = models.Servicio.objects.filter(id=int(id)).values_list('orden__id', 'orden__entrada').first()
                    if not tem_o:
                        return HttpResponse('{"info":"Not Order"}', content_type='application/json', status=204)
                    # end if
                    order = models.Orden.objects.filter(id=tem_o[0]).first()
                    if not servicio.estado:
                        servicios = models.Servicio.objects.filter(orden=order,status=True).latest('fin')
                        servicio.inicio = servicios.fin if servicios.fin is not None else tem_o[1]
                        servicio.comision = servicio.tipo.comision
                        servicio.valor = servicio.tipo.costo
                        servicio.fin = timezone.now()
                        servicio.estado = True
                        servicio.save()
                        order.valor = order.valor + servicio.valor
                        order.comision = order.comision + servicio.comision
                        order.save()
                        return HttpResponse('{"info":"Ok"}', content_type='application/json', status=200)
                    # end if
                    order.valor = order.valor - servicio.valor
                    order.comision = order.comision - servicio.comision
                    servicio.estado = False
                    servicio.save()
                    return HttpResponse('{"info":"Ok cancel"}', content_type='application/json', status=201)
                # end if
            # end if
        # end if
        return HttpResponse('{"info":"Not"}', content_type='application/json', status=204)
    # end def

    def post(self, request, *args, **kwargs):
        id = kwargs['pk']
        if re.match('^\d+$', id):
            orden = models.Orden.objects.filter(id=int(id)).first()
            if orden:
                orden.fin = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
                orden.pago = True
                orden.save()
                return HttpResponse('{"info":"Ok"}', content_type='application/json', status=200)
            # end if
        # end if
        return HttpResponse('{"info":"Not"}', content_type='application/json', status=204)
    # end def
# end class


class CancelService(supra.SupraFormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CancelService, self).dispatch(*args, **kwargs)
    # end def

    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        if re.match('^\d+$', id):
            servicio = models.Servicio.objects.filter(id=int(id)).first()
            if servicio:
                servicio.status = False
                servicio.save()
                return HttpResponse('{"info":"Ok "}', content_type='application/json', status=201)
            # end if
        # end if
        return HttpResponse('{"info":"Not"}', content_type='application/json', status=204)
    # end def

    def post(self, request, *args, **kwargs):
        id = kwargs['pk']
        if re.match('^\d+$', id):
            servicio = models.Servicio.objects.filter(id=int(id)).first()
            if servicio:
                servicio.status = False
                servicio.save()
                return HttpResponse('{"info":"Ok "}', content_type='application/json', status=201)
            # end if
        # end if
        return HttpResponse('{"info":"Not"}', content_type='application/json', status=204)
    # end def
# end class


class GetOrdenesPendientes(supra.SupraListView):
    model = cliente.Vehiculo
    list_display = ['ordenv', 'placa', 'marca', 'kilometraje', 'color', 'nombre', 'apellidos', 'cedula', 'celular', 'tipov', 'tipo', 'id']
    paginate_by = 5

    class Renderer:
        ordenv = 'orden__id'
        cedula = 'cliente__identificacion'
        nombre = 'cliente__nombre'
        apellidos = 'cliente__apellidos'
        tipov = 'tipo__nombre'
        celular = 'cliente__celular'
    # end class

    def get_queryset(self):
        queryset = super(GetOrdenesPendientes, self).get_queryset()
        return queryset.filter(orden__cerrada=False)
    # end def
# end class


class ImprimirOrden(supra.SupraFormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ImprimirOrden, self).dispatch(*args, **kwargs)
    # end def

    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        orden = models.Orden.objects.filter(id=int(id)).first()
        servicio = models.Servicio.objects.filter(orden__id=int(id))
	usuario = '%s %s'%(request.user.first_name,request.user.last_name)
        return render(request,'operacion/imprimirorden.html',{'o':orden, 's':servicio,'usuario':usuario})
    # end def

# end class


class ServiciosOrden(supra.SupraListView):
    model = models.Servicio
    list_display = ['servicio', 'placa','costo','identificacion','nombre','apellidos','orden_id']
    search_key = 'q'
    list_filter = ['orden__id']
    search_fields = ['orden__id']
    paginate_by = 1000

    class Renderer:
        servicio = 'tipo__nombre'
        placa = 'orden__vehiculo__placa'
        identificacion = 'orden__vehiculo__cliente__identificacion'
        nombre = 'orden__vehiculo__cliente__nombre'
        apellidos = 'orden__vehiculo__cliente__apellidos'
        costo = 'tipo__costo'
        orden_id = 'orden__id'
    # end class
# end class

class ReporteMServicio(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        # do something
        return super(ReporteMServicio, self).dispatch(*args, **kwargs)
    # end def

    def get(self, request):
        id_emp=request.GET.get('id', '0')
        ini=request.GET.get('ini', '2015-01-01')
        fin=request.GET.get('fin', '%s-%s-%s' %
                              (date.today().year, date.today().month, date.today().day))
        """
        f1=ini.split('-')
        f2=fin.split('-')
        d1='%s-%s-%s' % (f1[2], f1[0], f1[1])
        d2='%s-%s-%s' % (f2[2], f2[0], f2[1])
        """
        estado=request.GET.get('estado', False)
        r=0
        lista=list()
        response=HttpResponse(content_type='text/csv')
        response[
            'Content-Disposition']='attachment; filename="Reporte Servicio mas demorados .csv"'
        writer=csv.writer(response)
        writer.writerow(['Luxury'.encode('utf-8')])
        writer.writerow(['Fecha de inicio para el reporte'.encode('utf-8'), ''.encode(
            'utf-8'), ''.encode('utf-8'), 'Fecha de fin para el reporte'.encode('utf-8')])
        lista.append(u'Servicio'.encode('utf-8'))
        lista.append(u'Minutos'.encode('utf-8'))
        writer.writerow(lista)
        sql='''select get_tiempo_servicio('2016-11-15','2016-12-01')'''
        cursor=connection.cursor()
        cursor.execute(sql)
        row=cursor.fetchone()
        print row[0]
        rt = row[0]
        r=0
        while r <len( rt):
            li=list()
            li.append((rt[r]['nombre']).encode('utf-8'))
            li.append((rt[r]['total']).encode('utf-8'))
            writer.writerow(li)
            r=r + 1
        # end for
        return response
    # end class
# end class
