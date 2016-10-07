from django.conf.urls import url
import views


# url ws de tipo de servicios porvehiculo
urlpatterns = [
    url(r'^ws/tipo/servicio/$', views.TiposServicios.as_view(), name='ws_tipo_servicio'),
]

# url de registro, edicion de orden
urlpatterns += [
    url(r'^add/orden/$', views.AddOrdenForm.as_view(), name='addorden'),
    url(r'^edit/orden/(?P<pk>\d+)/$', views.AddOrdenForm.as_view(), name='editorden'),
    url(r'^close/orden/(?P<pk>\d+)/$', views.CloseOrden.as_view(), name='closeorden'),
]

# lista de servicion por orden
urlpatterns += [
    url(r'^ws/servicios/orden/$', views.WsServiciosOrden.as_view(), name='wsservorden'),
]

# lista de servicion por orden
urlpatterns += [
    url(r'^add/servicio/$', views.AddServicio.as_view(), name='addservicio'),
    url(r'^edit/servicio/(?P<pk>\d+)/$', views.AddServicio.as_view(), name='editservicio'),
    url(r'^ok/servicio/(?P<pk>\d+)/$', views.OkService.as_view(), name='okservice'),
]
