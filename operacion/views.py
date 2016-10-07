from django.shortcuts import render
from supra import views as supra
import models
import forms
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse
from django.views.generic import TemplateView
from datetime import date, timedelta, datetime
import re
from django.utils import timezone


class TiposServicios(supra.SupraListView):
    model = models.TipoServicio
    list_display = ['id', 'nombre']
    search_key = 'q'
    list_filter = ['vehiculos__id']
    search_fields = ['vehiculos__id']
    paginate_by = 1000
# end class


class AddOrdenForm(supra.SupraFormView):
    model = models.Orden
    form_class = forms.AddOrdenForm
    template_name = 'operacion/addorden.html'
# end class


class CloseOrden(supra.SupraFormView):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CloseOrden, self).dispatch(*args, **kwargs)
    # end def

    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        if re.match('^\d+$', id):
            orden = models.Orden.objects.filter(id=int(id)).first()
            if orden:
                orden.fin = timezone.now()
                orden.pago = True
                orden.save()
                return HttpResponse('{"info":"Ok"}', content_type='application/json', status=200)
            # end if
        # end if
        return HttpResponse('{"info":"Not"}', content_type='application/json', status=204)
    # end def

    def post(self, request, *args, **kwargs):
        id = kwargs['pk']
        print id,"llegada"
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
    list_display = ['id', 'valor', 'tipos', 'estado']
    list_filter = ['orden__id']
    search_fields = ['orden__id']
    paginate_by = 1000

    class Renderer:
        tipos = 'tipo__nombre'
    # end class
# end class


class AddServicio(supra.SupraFormView):
    model = models.Servicio
    form_class = forms.AddServicioForm
    template_name = 'operacion/addservicio.html'
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
                if not servicio.estado:
                    tem_o = models.Servicio.objects.filter(id=int(id)).values_list('orden__id', 'orden__entrada').first()
                    if not tem_o:
                        return HttpResponse('{"info":"Not Order"}', content_type='application/json', status=204)
                    # end if
                    order = models.Orden.objects.filter(id=tem_o[0]).first()
                    servicios = models.Servicio.objects.filter(orden=order).latest('fin')
                    servicio.inicio = servicios.fin if servicios else tem_o[1]
                    servicio.comision = servicio.tipo.costo*(servicio.tipo.comision/100)
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
                servicio.estado = False
                servicio.save()
                return HttpResponse('{"info":"Ok cancel"}', content_type='application/json', status=201)
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
