from django.shortcuts import render
import models
from supra import views as supra
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.views import logout
from django.shortcuts import HttpResponse
from django.views.generic import TemplateView
from supra import views as supra


# Create your views here.
class Login(supra.SupraSession):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        obj = super(Login, self).dispatch(request, *args, **kwargs)
        if request.user.is_authenticated():
            if not models.Recepcionista.objects.filter(id=request.user.id).first():
                return HttpResponse('{"res":"No cuenta con los permisos"}', content_type="application/json", status=201)
            # end def
        # end if
        return obj
    # end def
# end class


class Logout(TemplateView):
    #
    def dispatch(self, request, *args, **kwargs):
        logout(request, **kwargs)
        return HttpResponse('{"res":"ok"}', content_type="application/json", status=201)
    # end def
# end class


class WsOperarios(supra.SupraListView):
    model = models.Empleado
    list_display = ['nombre', 'id']
    paginate_by = 1000

    class Renderer:
        apellidos = 'last_name'
    # end class

    def nombre(self, obj, row):
        return '%s %s' % (obj.first_name, obj.last_name)
    # end def

    def get_queryset(self):
        queryset = super(WsOperarios, self).get_queryset()
        return queryset
# end class
