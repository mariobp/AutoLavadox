from django.shortcuts import render
from supra import views as supra
import models


class TiposServicios(supra.SupraListView):
    model = models.TipoServicio
    list_display = ['id', 'nombre']
    paginate_by = 100000
# end class
