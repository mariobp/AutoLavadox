from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
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


class VehiculoAdd(supra.SupraFormView):
    model = models.Vehiculo

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        motorizado = request.POST.get('motorizado', '')
        n_pedido = request.POST.get('pedido', 0)
        pedido = models.PedidoWS.objects.filter(
            id=n_pedido, motorizado__motorizado__identifier=motorizado).first()
        if pedido:
            models.PedidoWs.objects.filter(
                id=int(n_pedido)).update(activado=False)
            return super(CancelarPWService, self).dispatch(request, *args, **kwargs)
        # end if
        return HttpResponse('[{"status":false}]', content_type='application/json', status=404)
    # end def
# end class
