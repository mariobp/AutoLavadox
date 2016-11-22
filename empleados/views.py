#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
import models
from supra import views as supra
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.views import logout
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from supra import views as supra
from django.contrib.auth import login, logout, authenticate
from django.views.generic import View
import csv
import xlwt
import re
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.db import connection


# Create your views here.

class Login(supra.SupraSession):
    #model = models.Recepcionista
    template_name = "empleados/login.html"

    def form_valid(self, form):
        instance = form.save()
        for inline in self.validated_inilines:
            inline.instance = instance
            inline.save()
        # end for
        nex = self.request.GET.get('next', False)
        if nex:
            return HttpResponseRedirect(nex)
        return HttpResponseRedirect('/')
    # end def

    def login(self, request, cleaned_data):
        user = authenticate(username=cleaned_data[
                            'username'], password=cleaned_data['password'])
        if user is not None:
            exist_obj = self.model.objects.filter(pk=user.pk).count()
            if exist_obj and user.is_active:
                login(request, user)
                return user
            # end if
        # end if
        return HttpResponseRedirect('/empleados/login/')
        # end def

    def form_invalid(self, form):
        errors = dict(form.errors)
        print errors
        for i in self.invalided_inilines:
            errors['inlines'] = list(i.errors)
        # end for
        return render(self.request, self.template_name, {"form": form})
    # end def
# end class


class Logout(TemplateView):
    #
    def dispatch(self, request, *args, **kwargs):
        logout(request, **kwargs)
        return HttpResponseRedirect('/')
    # end def
# end class


class WsOperariosServicio(supra.SupraListView):
    model = models.Empleado
    search_key = 'q'
    list_display = ['id']
    search_fields = ['id']
    paginate_y = 1000

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(WsOperariosServicio, self).dispatch(*args, **kwargs)
    # end def

    def get_queryset(self):
        queryset = super(WsOperariosServicio, self).get_queryset()
        r = self.request.GET.get('q', False)
        return queryset.filter(servicio__id=r if re.search('^\d+$',r) else 0)
    # end def
# end class


class WsOperarios(supra.SupraListView):
    model = models.Empleado
    list_display = ['nombre', 'id']
    paginate_by = 1000

    class Renderer:
        apellidos = 'last_name'
    # end class

    def nombre(self, obj, row):
        return '%s %s' % (obj.first_name, obj.last_name)
    # end def

    def get_queryset(self):
        queryset = super(WsOperarios, self).get_queryset()
        return queryset.order_by('first_name', 'last_name')
# end class


class Excel(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(Excel, self).dispatch(*args, **kwargs)
    # end def
    def post(self, request):
        id_emp = request.GET.get('id', '0')
        ini = request.GET.get('inicio', '2015-01-01')
        fin = request.GET.get('fin', '%s-%s-%s' %
                              (date.today().year, date.today().month, date.today().day))
        estado = request.GET.get('estado', False)
        # CURSOR DE LA INFO EMPLEADO
        """
        cursor = connection.cursor()
        cursor.execute(
                    'select get_info_empleados_report_act(%s,\'%s\',\'%s\',%s)' % (id_emp, ini, fin,'true' if estado else 'false'))

        row = cursor.fetchone()
        res = row[0]
        """
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Reporte Empleado.csv"'
        #
        writer = csv.writer(response)
        writer.writerow(['Trabajador no encontrado'])
        return response

    def get(self, request):
        print request.GET
        id_emp = request.GET.get('id', '0')
        ini = request.GET.get('ini', '2015-01-01')
        fin = request.GET.get('fin', '%s-%s-%s' %
                              (date.today().year, date.today().month, date.today().day))
        f1= ini.split('-')
        f2= fin.split('-')
        d1 ='%s-%s-%s'%(f1[2],f1[0],f1[1])
        d2 ='%s-%s-%s'%(f2[2],f2[0],f2[1])
        estado = request.GET.get('estado', False)
        # CURSOR DE LA INFO EMPLEADO
        sql = """select ts.nombre from public.cliente_tipovehiculo as tv
                inner join public.operacion_tiposervicio_vehiculos as ts_tv
                on(tv.id=ts_tv.tipovehiculo_id)
                inner join public.operacion_tiposervicio as ts
                on (ts.id=ts_tv.tiposervicio_id) order by ts_tv.tipovehiculo_id asc,ts.id"""
        cursor = connection.cursor()
        cursor.execute(sql)
        row = cursor.fetchall()
        print row[0]
        r=0
        lista =list()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Reporte Empleados.csv"'
        writer = csv.writer(response)
        writer.writerow(['Luxury Service Car Zone'.encode('utf-8')])
        writer.writerow(['Fecha de inicio para el reporte'.encode('utf-8'),d1.encode('utf-8'),''.encode('utf-8'),''.encode('utf-8'),'Fecha de fin para el reporte'.encode('utf-8'),d2.encode('utf-8')])
        lista.append(u'Identificacion'.encode('utf-8'))
        lista.append(u'Nombre'.encode('utf-8'))
        lista.append(u'Apellidos'.encode('utf-8'))
        while  r < len(row):
            lista.append((row[r][0]).encode('utf-8'))
            r=r+1
        # end for
        lista.append('TOTAL'.encode('utf-8'))
        writer.writerow(lista)
        sql = """
        select u.id,p.identificacion,u.first_name as nombre, u.last_name from public.empleados_empleado as o
                 inner join public.auth_user as u on (o.persona_ptr_id=u.id)
                 inner join public.empleados_persona as p on (p.user_ptr_id=u.id)"""
        cursor.execute(sql)
        row = cursor.fetchall()
        cursor2 = connection.cursor()
        r=0
        while  r < len(row):
            li = list()
            li.append(row[r][1])
            li.append(row[r][2])
            li.append(row[r][3])
            sql2="""select* from(select ts.id,ts.nombre,ts_tv.tipovehiculo_id as tipo,
                       sum(
                          case when s.id is null then 0
                                when s.status=false then 0
                                when s.estado=false then 0
                                when ts.comision <=0 then 0
                                else (ts.costo*ts.comision/100) end ) as total from (select * from public.empleados_empleado as r where r.persona_ptr_id="""+str(row[r][0])+""") as o
                   cross join public.cliente_tipovehiculo  as tv
                   inner join public.operacion_tiposervicio_vehiculos as ts_tv
                   on(tv.id=ts_tv.tipovehiculo_id)
                   inner join public.operacion_tiposervicio as ts
                   on (ts.id=ts_tv.tiposervicio_id)
                   left join public.operacion_servicio as s on (s.tipo_id=ts.id and s.status=true and o.persona_ptr_id=s.operario_id and s.inicio::timestamp::date >= '"""+d1+"""'::date and s.inicio::timestamp::date <= '"""+d2+""""'::date)
                   group by ts.id,ts.nombre,ts_tv.tipovehiculo_id) as tabla
                   order by tabla.tipo asc,tabla.id asc"""
            cursor2.execute(sql2)
            row2= cursor2.fetchall()
            i=0
            suma=0
            while i < len(row2):
                li.append(row2[i][3])
                suma=suma+ row2[i][3]
                i=i+1
            # end while
            li.append(suma)
            writer.writerow(li)
            r=r+1
        # end for

        # Create the HttpResponse object with the appropriate CSV header.

        #
        return response

    # end def
# end class


class ExcelEmpleados(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ExcelEmpleados, self).dispatch(*args, **kwargs)
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
        """
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
        """
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=Reporte tiempo empleados.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("Empleados")
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        sql='select informe_time_operarios(\'%s\', \'%s\')'%(ini,fin)
        cursor=connection.cursor()
        cursor.execute(sql)
        row=cursor.fetchone()
        rt = row[0][0]
        r=0
        servicios = rt['servicios']
        operarios = rt['empleados']
        li=list()
        ws.write(0,1,'Luxury'.encode('utf-8'),font_style)
        ws.write(1,0,'Fecha de inicio para el reporte'.encode('utf-8'), font_style)
        ws.write(1,1,ini.encode('utf-8'), font_style)
        ws.write(1,2,'Fecha de fin para el reportee'.encode('utf-8'), font_style)
        ws.write(1,3,fin.encode('utf-8'), font_style)
        exc_row=2
        while r <len(servicios):
            ws.write(exc_row, r, (servicios[r]['nombre']).encode('utf-8'), font_style)
            r=r + 1
        # end for
        exc_row = exc_row + 1
        # writer.writerow(li)
        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 1
        i=0
        while i < len(operarios):
            j = 0
            ws.write(exc_row, j, (operarios[i]['identificacion']).encode('utf-8'), font_style)
            j = j + 1
            ws.write(exc_row, j, (operarios[i]['first_name']).encode('utf-8'), font_style)
            j = j + 1
            ws.write(exc_row, j, (operarios[i]['last_name']).encode('utf-8'), font_style)
            j = j + 1
            ws.write(exc_row, j, (operarios[i]['telefono']).encode('utf-8'), font_style)
            j = j + 1
            servi = operarios[i]['servicios']
            print servi
            while j < len(servi):
                ws.write(exc_row, j, (servi[j-4]['total']), font_style)
                j = j + 1
            # end while
            i = i + 1
            exc_row = exc_row + 1
        # end for
        wb.save(response)
        return response
    # end class
# end class
