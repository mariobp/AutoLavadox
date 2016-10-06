from django.shortcuts import render
from supra import views as supra
import models


class TiposVehiculos(supra.SupraListView):
    model = models.TipoVehiculo
    list_display = ['id', 'nombre']
    paginate_by = 100000
# end class


class VehiculoInfo(supra.SupraListView):
    model = models.Vehiculo
    search_key = 'q'
    list_display = ['placa', 'cliente__nombre', 'cliente__apellidos']
    search_fields = ['placa']
    list_filter = ['placa']
    paginate_by = 1
# end if
