# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from supra import views as supra
import models
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import re
from django.shortcuts import HttpResponse
from django.views.generic import TemplateView
import forms


class TiposVehiculos(supra.SupraListView):
    model = models.TipoVehiculo
    list_display = ['id', 'nombre']
    paginate_by = 100000
# end class


class VehiculoInfo(supra.SupraListView):
    model = models.Vehiculo
    search_key = 'q'
    list_display = ['placa', 'nombre', 'apellidos', 'cedula', 'tipov']
    search_fields = ['placa']
    list_filter = ['placa']
    paginate_by = 1

    class Renderer:
        cedula = 'cliente__identificacion'
        nombre = 'cliente__nombre'
        apellidos = 'cliente__apellidos'
        tipov = 'tipo__nombre'
# end if


class VehiculoAdd(supra.SupraFormView):
    model = models.Vehiculo
    form_class = forms.AddVehivuloForm
    template_name = 'cliente/addvehiculo.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(VehiculoAdd, self).dispatch(request, *args, **kwargs)
    # end def
# end class


def validNum(cad):
    return re.match('^\d+$', cad)
