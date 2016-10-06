from django.shortcuts import render
from supra import views as supra
import models
import forms
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class TiposServicios(supra.SupraListView):
    model = models.TipoServicio
    search_key = 'q'
    list_display = ['id', 'nombre']
    paginate_by = 10

    def get_queryset(self):
        super(TiposServicios, self).get_queryset()
        print self.request
        query = queryset.filter(vehiculo__id=10)
        print query
        return query
    # end def
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

    def post(self, request, *args, **kwargs):
        return HttpResponse('jaja')
    # end def
# end class
