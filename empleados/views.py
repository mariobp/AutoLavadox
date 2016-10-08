from django.shortcuts import render
import models
from supra import views as supra
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.views import logout
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from supra import views as supra
from django.contrib.auth import login, logout, authenticate


# Create your views here.

class Login(supra.SupraSession):
    #model = models.Recepcionista
    template_name = "empleados/login.html"

    def form_valid(self, form):
        instance = form.save()
        for inline in self.validated_inilines:
            inline.instance = instance
            inline.save()
        # end for
        nex = self.request.GET.get('next', False)
        if nex:
            return HttpResponseRedirect(nex)
        return HttpResponseRedirect('/')
    # end def

    def login(self, request, cleaned_data):
        user = authenticate(username=cleaned_data[
                            'username'], password=cleaned_data['password'])
        if user is not None:
            exist_obj = self.model.objects.filter(pk=user.pk).count()
            if exist_obj and user.is_active:
                login(request, user)
                return user
            # end if
        # end if
        return HttpResponseRedirect('/empleados/login/')
        # end def

    def form_invalid(self, form):
        errors = dict(form.errors)
        print errors
        for i in self.invalided_inilines:
            errors['inlines'] = list(i.errors)
        # end for
        return render(self.request, self.template_name, {"form": form})
    # end def
# end class


class Logout(TemplateView):
    #
    def dispatch(self, request, *args, **kwargs):
        logout(request, **kwargs)
        return HttpResponseRedirect('/')
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
