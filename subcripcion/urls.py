from django.conf.urls import url
import views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


# servicios de planes
urlpatterns = [
    url(r'^get/planes/$', login_required(views.ListPlan.as_view()), name='list_planes'),
    url(r'^add/plan/$', login_required(views.AddPlan.as_view()), name='add_plan'),
    url(r'^edit/plan/(?P<pk>\d+)/$',
        login_required(views.AddPlan.as_view()), name='edit_plan'),
    url(r'^delete/plan/(?P<pk>\d+)/$',
        login_required(views.AddPlan.as_view()), name='delete_plan'),
]

# servicios de Clientes
urlpatterns += [
    url(r'^get/cliente/$', login_required(views.ListCliente.as_view()),
        name='list_cliente'),
    url(r'^add/cliente/$', login_required(views.AddCliente.as_view()),
        name='add_cliente'),
    url(r'^edit/cliente/(?P<pk>\d+)/$',
        login_required(views.EditCliente.as_view()), name='edit_cliente'),
    url(r'^delete/cliente/(?P<pk>\d+)/$',
        login_required(views.DeleteCliente.as_view()), name='delete_cliente'),
    url(r'^change/pass/empleados/',
        login_required(views.SetPassWordEmpleado.as_view()), name='set_pass_empleado'),
]

# servicios de instancias de modulos
urlpatterns += [
    url(r'^get/itmodulo/$', login_required(views.ListInstModulo.as_view()),
        name='list_instmodulo'),
]

# servicios de instancias de modulos
urlpatterns += [
    url(r'^add/suscripcion/$',
        login_required(views.AddSuscripcion.as_view()), name='add_suscripcion'),
]
