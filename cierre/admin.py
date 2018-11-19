from django.contrib import admin
from exileui.admin import exileui, ExStacked, ExTabular, DateRangeEX
import models
from django.utils.html import format_html
import forms
from django.db import connection
import json
from autolavadox import service
from autolavadox.settings import SERVER_STATIC
from autolavadox.views import set_queryset, get_cuenta
from django.db.models import Q
from autolavadox.service import Service
# Register your models here.


class BaseAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super(BaseAdmin, self).get_queryset(request)
        queryset= set_queryset(queryset)
        return queryset.order_by('-id')
    # end def
#end class


class TipoServicioAdmin(BaseAdmin):
    form = forms.AddTipoServicioForm
    list_display = ['id_cierre','inicio','fin','total','comision','accion_reporte', 'cuenta']
    list_filter = ['id','inicio','fin',]
    search_fields = ['id','inicio','fin','total']
    list_display_links = ('id_cierre',)

    def id_cierre(self, obj):
        i = 0
        men = ''
        while i < 10 - len(str(obj.pk)):
            men = men + '0'
            i = i+1
        # end ford
        return '%s%d' % (men, obj.pk)
    # end def

    def accion_reporte(self, obj):
        return format_html("<a href='/cierre/factura/tipo/{0}/' class='generar addlink'>Imprimir</a>", obj.id)
    # end def

    def save_model(self, request, obj, form, change):
        cursor = connection.cursor()
        cuenta,cuenta = get_cuenta()
        if cuenta:
            cuenta_id = Service.getCuenta().id
            cursor.execute('select cierre_factura_total_cuenta(\'%s\',\'%s\',%d::integer)'%(str(obj.inicio),str(obj.fin),cuenta_id))
        else:
            cursor.execute('select cierre_factura_total(\'%s\',\'%s\')'%(str(obj.inicio),str(obj.fin)))
        #end if
        row = cursor.fetchone()
        r = row[0][0]
        obj.total=r['total']
        obj.comision=r['comosion']
        obj.save()
    # end def

    class Media:
        js = ('{}/static/cierre/js/cierre.js'.format(SERVER_STATIC),)
    # end class

    id_cierre.allow_tags = True
    id_cierre.short_description = 'Cierre Id'
    accion_reporte.allow_tags = True
    accion_reporte.short_description = 'Reporte Dia'
# end class


class FacturaAdmin(BaseAdmin):
    form = forms.AddTipoServicioForm
    list_display = ['id_cierre','inicio','fin','total','comision','accion_reporte', 'cuenta']
    list_filter = ['id','inicio','fin',]
    search_fields = ['id','inicio','fin','total']
    list_display_links = ('id_cierre',)

    def id_cierre(self, obj):
        i = 0
        men = ''
        while i < 10 - len(str(obj.pk)):
            men = men + '0'
            i = i+1
        # end ford
        return '%s%d' % (men, obj.pk)
    # end def

    def accion_reporte(self, obj):
        return format_html("<a href='/cierre/factura/{0}/' class='generar addlink'>Imprimir</a>", obj.id)
    # end def

    def save_model(self, request, obj, form, change):
        obj.save()
        cursor = connection.cursor()
        cursor.execute('select cierre_factura_total(\'%s\',\'%s\')'%(str(obj.inicio),str(obj.fin)))
        row = cursor.fetchone()
        r = row[0][0]
        obj.total=r['total']
        obj.comision=r['comosion']
        obj.save()
    # end def

    class Media:
        js = ('/static/cierre/js/cierre.js',)
    # end class

    id_cierre.allow_tags = True
    id_cierre.short_description = 'Cierre Id'
    accion_reporte.allow_tags = True
    accion_reporte.short_description = 'Reporte Dia'
# end class


class TurnoAdmin(BaseAdmin):
    list_display = ['nombre', 'inicio', 'fin', 'cuenta']
    search_fields = ['nombre', 'inicio', 'fin', 'cuenta__cliente__nombre']
    form = forms.TurnoAdminForm

    def get_form(self, request, obj=None, *args, **kwargs):
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if not admin:
            kwargs['form'] = forms.TurnoForm
        # end if
        return super(TurnoAdmin, self).get_form(request, obj, *args, **kwargs)
    # end def


class CierreAdmin(BaseAdmin):
    list_display = ['turno', 'inicio', 'fin', 'total', 'comision', 'producto', 'cuenta', 'imprimir_cierre']
    search_fields = ['turno__nombre', 'cuenta__cliente__nombre']
    form = forms.CierreAdminForm

    def get_readonly_fields(self, request, obj=None):
        """ Set readonly attributes
         subproject is readonly when the object already exists
         fields are always readonly
        """
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if obj:
            return ('cuenta', 'total',  'comision')
        if admin:
            return ['turno', 'inicio', 'fin', 'total',  'comision']
        return ('total',  'comision',)

    class Media:
        js = ('/static/cierre/js/turno.js',)
    # end class

    def get_form(self, request, obj=None, *args, **kwargs):
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if not admin:
            kwargs['form'] = forms.CierreForm
        # end if
        return super(CierreAdmin, self).get_form(request, obj, *args, **kwargs)
    # end def

    def imprimir_cierre(self, obj):
        return format_html("<a href='/cierre/factura/turno/{0}/' class='imprimir'><i class='micon'>print</i>Imprimir</a>", obj.id)
    # end def


    def save_model(self, request, obj, form, change):
        #obj.save()
        cursor = connection.cursor()
        sql = 'select get_cierre_turno(%d,%d)' % (obj.id, obj.cuenta.id)
        cursor.execute(sql)
        # end if
        row = cursor.fetchone()
        resul = row[0][0]
        obj.comision = resul['total'][0].get('comision') if resul['total'] else 0
        obj.total = resul['total'][0].get('total') if resul['total'] else 0
        obj.producto = resul['productos_total'][0].get('total') if resul['productos_total'] else 0
        obj.save()
    # end if

    imprimir_cierre.allow_tags = True
    imprimir_cierre.short_description = 'Imprimir'

exileui.register(models.TipoServicio, TipoServicioAdmin)
exileui.register(models.Factura, FacturaAdmin)
exileui.register(models.Turno, TurnoAdmin)
exileui.register(models.Cierre, CierreAdmin)
