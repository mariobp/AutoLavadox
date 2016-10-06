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
    list_filter = ['vehiculos__id']
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
        print id,"llegada"
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
