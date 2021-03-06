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
    list_display = ['placa', 'marca', 'kilometraje', 'color', 'nombre', 'apellidos', 'cedula', 'celular', 'tipov', 'tipo', 'id']
    search_fields = ['placa']
    list_filter = ['placa']
    paginate_by = 5

    class Renderer:
        cedula = 'cliente__identificacion'
        nombre = 'cliente__nombre'
        apellidos = 'cliente__apellidos'
        tipov = 'tipo__nombre'
        celular = 'cliente__celular'
    # end class
# end class# end if


class VehiculoAdd(supra.SupraFormView):
    model = models.Vehiculo
    form_class = forms.AddVehivuloForm
    template_name = 'cliente/addvehiculo.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(VehiculoAdd, self).dispatch(request, *args, **kwargs)
    # end def
# end class


class VehiculoEdit(supra.SupraFormView):
    model = models.Vehiculo
    form_class = forms.EditVehivuloForm
    template_name = 'cliente/addvehiculo.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(VehiculoEdit, self).dispatch(request, *args, **kwargs)
    # end def
# end class


def validNum(cad):
    return re.match('^\d+$', cad)


class VehiculoInline(supra.SupraInlineFormView):
    base_model = models.Cliente
    model = models.Vehiculo
# end class


class ClienteSupra(supra.SupraFormView):
    model = models.Cliente
    form_class = forms.AddClienteForm
    inlines = [VehiculoInline]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ClienteSupra, self).dispatch(request, *args, **kwargs)
    # end def
# end class


class ClienteList(supra.SupraListView):
    model = models.Cliente
    search_key = 'q'
    list_display = ['id', 'nombre', 'apellidos', 'identificacion', 'celular']
    search_fields = ['identificacion', 'celular']

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ClienteList, self).dispatch(request, *args, **kwargs)
    # end def
# end class
