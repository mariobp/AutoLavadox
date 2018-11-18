# -*- coding: utf-8 -*-
from django.contrib import admin
from exileui.admin import exileui, ExStacked, ExTabular, DateRangeEX
import models
import forms
from datetime import datetime
from daterange_filter.filter import DateRangeFilter
from django.utils.html import format_html
from import_export.admin import ImportExportMixin, ExportMixin
from import_export.resources import ModelResource
from import_export.formats import base_formats
import report
from import_export import fields
import time
from datetime import date, timedelta
import datetime
from autolavadox.service import Service
from django.db.models import Q
from autolavadox.views import BaseAdmin, set_queryset
from autolavadox import settings, service
from inventario import models  as inventario

# Register your models here.


class ServicioInline(admin.StackedInline):
    model = models.Servicio
    form = forms.ServicioInlineForm
    formset = forms.SerivioInlineFormset
    extra = 2
# end class


class ProductoVentaInlineAdmin(admin.StackedInline):
    model = models.ProductoVenta
    form = forms.ProductoVentaInlineForm
    formset = forms.ProductoVentaInlineFormset
    extra = 2


class Serviciossource(ModelResource):
    Nombre = fields.Field()
    Operario = fields.Field()
    Valor = fields.Field()
    Comision = fields.Field()

    class Meta:
        model = models.Servicio
        fields = ('inicio','fin')

    def dehydrate_Nombre(self, obj):
        return '%s ' % (obj.tipo.nombre)

    def dehydrate_Operario(self, obj):
        if obj.operario :
            re = ''
            for o in obj.operario.all():
                re = re + ('%s %s, '%(o.first_name,o.last_name))
            # end for
            return re
        # end if
        return '--- ----'

    def dehydrate_Valor(self, obj):
        return '%s ' % (obj.valor)

    def dehydrate_Comision(self, obj):
        return '%s ' % (obj.comision)


class ServicioAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['orden','placa_nombre',  'tipo', 'inicio', 'fin', 'valor', 'comision', 'estado']
    list_filter = [('inicio', DateRangeEX)]
    search_fields = ['orden__id', ]
    list_editable = ['estado']
    resource_class = Serviciossource
    formats = (base_formats.XLSX,base_formats.XLS,base_formats.CSV)
    form = forms.ServicioForm

    def get_readonly_fields(self, request, obj=None):
        """ Set readonly attributes
         subproject is readonly when the object already exists
         fields are always readonly
        """
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if obj:
            return ('cuenta',)
        if admin and not obj:
            return ('tipo' ,'orden', 'operario', )
        return ()

    def get_form(self, request, obj=None, *args, **kwargs):
        ser = Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if admin:
            kwargs['form'] = forms.ServicioAdminForm

        # end if
        return super(ServicioAdmin, self).get_form(request, obj, *args, **kwargs)

    def placa_nombre(self, obj):
        if obj.orden :
            if obj.orden.vehiculo :
                if obj.orden.vehiculo.placa :
                    return obj.orden.vehiculo.placa
                # end if
            # end if
        # end if
        return '-----'
    #

    def save_model(self, request, obj, form, change):
        obj.save()
        if obj.tipo:
            obj.comision = obj.tipo.comision
        obj.save()
    # end if

    def get_queryset(self, request):
        queryset = super(ServicioAdmin, self).get_queryset(request)
        """
        drf__inicio__gte = request.GET.get('drf__inicio__gte', False)
        drf__inicio__lte = request.GET.get('drf__inicio__lte', False)
        now = datetime.now()
        if not drf__inicio__gte and not drf__inicio__lte:
            return queryset.filter(
                inicio__year = now.year,
                inicio__month = now.month,
                inicio__day = now.day,
            )
        # end if
        """
        queryset = set_queryset(queryset)
        return queryset.filter(status=True).order_by('-id')
    # end def

    # end class

    placa_nombre.allow_tags = True
    placa_nombre.short_description = 'Placa'
# end class


class OrdenInforme(ModelResource):

    Identificador = fields.Field()
    Valor = fields.Field()
    Comision = fields.Field()
    Terminada = fields.Field()
    Pago = fields.Field()
    Vehiculo = fields.Field()


    class Meta:
        model = models.Orden
        fields = ('entrada','fin')
    # end class

    def dehydrate_Identificador(self, obj):
        i = 0
        men = ''
        while i < 10 - len(str(obj.pk)):
            men = men + '0'
            i = i+1
        # end ford
        t = '%s%d' % (str(men), obj.pk)
        print t
        return u'%s' % (t)
    # end def

    def dehydrate_Valor(self, obj):
        return '%s ' % (obj.valor)
    # end def

    def dehydrate_Comision(self, obj):
        return '%s ' % (obj.comision)
    # end def

    def dehydrate_Terminada(self, obj):
        return '%s ' % (str('Si') if obj.cerrada else str('No'))
    # end def

    def dehydrate_Pago(self, obj):
        return '%s ' % (str('Si') if obj.pago else str('No'))
    # end def

    def dehydrate_Vehiculo(self, obj):
        return '%s' % (obj.vehiculo.placa)
    # end def
# end class


class OrdenAdmin(ExportMixin, admin.ModelAdmin):
    inlines = [ServicioInline, ProductoVentaInlineAdmin]
    list_display = ['id_reporte', 'fecha_orden', 'fecha_orden_fin', 'vehiculo', 'nombre_cliente','identificacion_cliente', 'valor', 'comision', 'cancelada', 'cerrada', 'pago', 'imprimir_orden']
    list_filter = [('fin', DateRangeEX)]
    search_fields = ['entrada', 'vehiculo__placa','vehiculo__cliente__nombre', 'valor', 'comision', 'pago',]
    list_editable = ['cerrada', 'cancelada', 'pago', 'vehiculo']
    form = forms.OrdenAdminForm
    list_display_links = ['id_reporte']
    resource_class = OrdenInforme
    formats = (base_formats.XLSX,base_formats.XLS,base_formats.CSV)

    def get_readonly_fields(self, request, obj=None):
        """ Set readonly attributes
         subproject is readonly when the object already exists
         fields are always readonly
        """
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if obj:

            return ('cuenta',)
        if admin:
            return ('observacion',
            'vehiculo',
            'recepcionista',)
        return ()

    def get_form(self, request, obj=None, *args, **kwargs):
        ser = Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if not admin:
            kwargs['form'] = forms.OrdenForm
            # end if
        if obj and not admin:
            kwargs['form'] = forms.OrdenEditForm
        # end if
        return super(OrdenAdmin, self).get_form(request, obj, *args, **kwargs)
    # end def

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
        formset.save_m2m()

    def save_model(self, request, obj, form, change):
        #obj.save()
        total = 0
        comi = 0
        if obj.cuenta:
            if obj.cuenta.cliente:
                if obj.cuenta.cliente.inventario:
                    pv_operaciones = obj.historiadeserviciooperacion_set.all()
                    for pv_ope in pv_operaciones:
                        __pv_operacion = inventario.Operacion.objects.get(id=pv_ope.producto.id)
                        __pv_operacion.existencias = pv_ope.producto.existencias + pv_ope.cantidad
                        __pv_operacion.save()
                    obj.historiadeserviciooperacion_set.all().delete()
        for s in models.Servicio.objects.filter(orden=obj):
            if s.status and s.estado:
                print 'Entro en los productos'
                s.valor = s.tipo.costo
                s.comision = s.tipo.comision
                comi += s.comision
                total += s.valor
                s.save()
                composicion_ = s.tipo.composicionservicio_set.all().values_list('id', flat=True)
                if composicion_:
                    componentes = models.Componente.objects.filter(composicion__id__in=composicion_)
                    for component in componentes:
                        component.producto.existencias = component.producto.existencias - component.cantidad
                        component.producto.save()
                        historial_venta = models.HistoriaDeServicioOperacion(orden=obj, producto=component.producto, cantidad=component.cantidad)
                        historial_venta.save()
                    #end if
        # end for
        total_venta_productos = 0
        if obj.cuenta:
            if obj.cuenta.cliente:
                if obj.cuenta.cliente.inventario:
                    for pv in obj.historiadeservicioventa_set.all():
                        pv.producto.existencias = pv.producto.existencias + pv.cantidad
                        pv.producto.save()
                    obj.historiadeservicioventa_set.all().delete()
                    for pv in obj.productoventa_set.all():
                        pro_venta = models.HistoriaDeServicioVenta(orden=obj, producto=pv.producto, cantidad=pv.cantidad)
                        pro_venta.save()
                        total_venta_productos += pv.producto.precio_venta * pv.cantidad
                        pv.total = pv.producto.precio_venta * pv.cantidad
                        pv.save()
        obj.valor = total + total_venta_productos
        obj.comision = comi
        orden__ = models.Orden.objects.get(id=obj.id)
        orden__.valor = total + total_venta_productos
        orden__.comision = comi
        orden__.save()
        print 'Este debe ser el valor de la comision ', orden__.valor
        obj.save()
        super(OrdenAdmin, self).save_model(request, obj, form, change)
    # end if

    def id_reporte(self, obj):
        i = 0
        men = ''
        while i < 10 - len(str(obj.pk)):
            men = men + '0'
            i = i+1
        # end ford
        return '%s%d' % (men, obj.pk)
    # end def

    def imprimir_orden(self, obj):
        return format_html("<a href='{0}' class='imprimir'><i class='micon'>print</i>Imprimir</a>", obj.id)
    # end def

    def nombre_cliente(self, obj):
        if not obj.vehiculo:
            return '--- ---'
        if not obj.vehiculo.cliente:
            return '--- ---'
        return '%s %s'%(obj.vehiculo.cliente.nombre,obj.vehiculo.cliente.apellidos) if obj.vehiculo.cliente else '---- -----'
    #end

    def identificacion_cliente(self, obj):
        if not obj.vehiculo:
            return '--- ---'
        if not obj.vehiculo.cliente:
            return '--- ---'
        return '%s'%(obj.vehiculo.cliente.identificacion) if obj.vehiculo.cliente else '-------'
    #end

    def fecha_orden(self, obj):
        if obj.entrada:
            h = '0%d'%obj.entrada.hour if obj.entrada.hour <10 else '%d'%obj.entrada.hour
            m = '0%d'%obj.entrada.minute if obj.entrada.minute <10 else '%d'%obj.entrada.minute
            s = '0%d'%obj.entrada.second if obj.entrada.second <10 else '%d'%obj.entrada.second
            return '%d-%d-%d %s:%s:%s'%(obj.entrada.day,obj.entrada.month,obj.entrada.year,h,m,s)
        else:
            return '--/--/--'
    # end def

    def fecha_orden_fin(self, obj):
        if obj.fin :
            h = '0%d'%obj.fin.hour if obj.fin.hour <10 else '%d'%obj.fin.hour
            m = '0%d'%obj.fin.minute if obj.fin.minute <10 else '%d'%obj.fin.minute
            s = '0%d'%obj.fin.second if obj.fin.second <10 else '%d'%obj.fin.second
            return '%d-%d-%d %s:%s:%s'%(obj.fin.day,obj.fin.month,obj.fin.year,h,m,s)
        else:
            return '--/--/--'
    # end def

    def get_queryset(self, request):
        queryset = super(OrdenAdmin, self).get_queryset(request)
        print request.GET
        gte = request.GET.get('drf__fin__gte', False)
        lte = request.GET.get('drf__fin__lte', False)
        print lte, gte,"menor mayor"
        if gte and lte:
            c1 = gte.split('/')
            c2 = lte.split('/')
            d1 = datetime.datetime(int(c1[2]),int(c1[0]),int(c1[1]),0,0,0,0)
            d2 = datetime.datetime(int(c2[2]),int(c2[0]),int(c2[1]),0,0,0,0)
            if d1 == d2 :
                print "son iguales"
                return queryset.filter(
                    fin=d1
                )
            # end if
            """
            return queryset.filter(
                fin__range=[d1,d2]
            )
            """
            f1 = queryset.filter(
                fin__range=[d1,d2]
            )
            return f1
        # end if
        queryset = set_queryset(queryset)
        return queryset.order_by('-id')
    # end def

    class Media:
        js = ('/home/coviyarce/webapps/static_autolavadox/operacion/js/json3.min.js','/home/coviyarce/webapps/static_autolavadox/operacion/js/operacion.js',)
        css = {
            'all': ('/home/coviyarce/webapps/static_autolavadox/operacion/css/operacion.css',)
        }
    # end class

    imprimir_orden.allow_tags = True
    imprimir_orden.short_description = 'Imprimir Orden'
    nombre_cliente.allow_tags = True
    nombre_cliente.short_description = 'Propietario'
    identificacion_cliente.allow_tags = True
    identificacion_cliente.short_description = 'Identificacion'
    fecha_orden.allow_tags = True
    fecha_orden.short_description = 'Realización'
    fecha_orden_fin.allow_tags = True
    fecha_orden_fin.short_description = 'Finalización'
    id_reporte.allow_tags = True
    id_reporte.short_description = 'Factura'
# end class


class TipoInforme(ModelResource):

    Nombre = fields.Field()
    Costo = fields.Field()
    Comision = fields.Field()
    Tipo = fields.Field()


    class Meta:
        model = models.TipoServicio
        fields = ()
    # end class

    def dehydrate_Nombre(self, obj):
        return '%s ' % (obj.nombre)
    # end def

    def dehydrate_Costo(self, obj):
        return '%s ' % (obj.costo)
    # end def

    def dehydrate_Comision(self, obj):
        return '%s ' % (obj.comision)
    # end def

    def dehydrate_Tipo_Vehiculo(self, obj):
        r = 'No asociado'
        if obj.vehiculos :
            r = ''
            for x in obj.vehiculos.all :
                r = r + (', %s'%x.nombre)
            # end for
        # end if
        return '%s' % (str(r))
    # end def

# end class


class TipoAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('nombre','vehiculoTipo','costo', 'comision', 'state')
    search_fields = ['nombre','vehiculos__nombre']
    filter_horizontal = ('vehiculos',)
    resource_class = TipoInforme
    formats = (base_formats.XLSX,base_formats.XLS,base_formats.CSV)
    form = forms.AddTipoServicioFormAdmin

    def vehiculoTipo(self, obj):
        l = []
        for x in obj.vehiculos.all():
            l.append(x.nombre)
        #end for
        print ','.join([str(i) for i in l])
        return ','.join([str(i) for i in l]) if l  else 'No asignado.'
    # end def

    def get_readonly_fields(self, request, obj=None):
        """ Set readonly attributes
         subproject is readonly when the object already exists
         fields are always readonly
        """
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if obj and admin:
            return ('cuenta', )
        if admin:
            return ('nombre', 'vehiculos', 'costo', 'comision', 'state', )
        return ()


    def get_form(self, request, obj=None, *args, **kwargs):
        ser = Service.get_instance()
        tem_cuenta,is_user,admin = ser.isUser()
        if not admin :
            kwargs['form'] = forms.AddTipoServicioForm
        # end if
        return super(TipoAdmin, self).get_form(request, obj, *args, **kwargs)
    # end def

    def get_queryset(self, request):
        queryset = super(TipoAdmin, self).get_queryset(request)
        queryset= set_queryset(queryset)
        return queryset.filter(Q(state=True)).order_by('-id')
    # end def

    vehiculoTipo.allow_tags = True
    vehiculoTipo.short_description = 'Vehiculo'
# end class

exileui.register(models.TipoServicio, TipoAdmin)
exileui.register(models.Servicio, ServicioAdmin)
exileui.register(models.Orden, OrdenAdmin)

class ComponenteInlineAdmin(admin.StackedInline):
    model = models.Componente
    extra = 2
    form = forms.ComponenteInlineForm
    formset = forms.ComponenteInlineFormset


class ComposicionServicioAdmin(admin.ModelAdmin):
    inlines = [ComponenteInlineAdmin]
    list_display = ['servicio', 'cuenta']
    search_fields = ['cuenta__cliente__nombre', 'servicio__nombre']
    form = forms.ComposicionServicioAdminForm

    def get_form(self, request, obj=None, *args, **kwargs):
        ser = Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if not admin:
            kwargs['form'] = forms.ComposicionServicioForm
        # end if
        return super(ComposicionServicioAdmin, self).get_form(request, obj, *args, **kwargs)

    def get_queryset(self, request):
        queryset = super(ComposicionServicioAdmin, self).get_queryset(request)
        ser = Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if tem_cuenta and is_user:
            cuenta = ser.getCuenta()
            queryset = queryset.filter(cuenta=cuenta)
        # end if
        return queryset.order_by('-id')
    # end def

    def get_readonly_fields(self, request, obj=None):
        """ Set readonly attributes
         subproject is readonly when the object already exists
         fields are always readonly
        """
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if obj:

            return ('cuenta',)
        if admin:
            return ('servicio',)
        return ()


class ComponenteAdmin(admin.ModelAdmin):
    list_display = ['composicion', 'producto', 'cantidad', 'cuenta']
    search_fields = ['cuenta__cliente__nombre', 'producto__nombre', 'composicion__servicio__nombre']
    form = forms.ComponenteAdminForm

    def get_form(self, request, obj=None, *args, **kwargs):
        ser = Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if not admin:
            kwargs['form'] = forms.ComponenteForm
        # end if
        return super(ComponenteAdmin, self).get_form(request, obj, *args, **kwargs)

    def get_queryset(self, request):
        queryset = super(ComponenteAdmin, self).get_queryset(request)
        ser = Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if tem_cuenta and is_user:
            cuenta = ser.getCuenta()
            queryset = queryset.filter(cuenta=cuenta)
        # end if
        return queryset.order_by('-id')
    # end def

    def get_readonly_fields(self, request, obj=None):
        """ Set readonly attributes
         subproject is readonly when the object already exists
         fields are always readonly
        """
        ser = service.Service.get_instance()
        tem_cuenta, is_user, admin = ser.isUser()
        if obj:
            return ('cuenta',)
        if admin:
            return ('composicion', 'producto', 'cantidad', )
        return ()

exileui.register(models.ComposicionServicio, ComposicionServicioAdmin)
