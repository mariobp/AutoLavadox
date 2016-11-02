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
        return queryset
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
        while  r < len(row):
            lista.append(row[r][0])
            r=r+1
        # end for
        writer.writerow(lista)
        # Create the HttpResponse object with the appropriate CSV header.

        #
        return response

    # end def
# end class
