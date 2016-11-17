from django.conf.urls import url
import views

# url de tipo de vehiculos
urlpatterns = [
    url(r'^tipo/vehiculo/$', views.TiposVehiculos.as_view(), name='tipo_vehiculo'),
    url(r'^vehiculo/$', views.VehiculoInfo.as_view(), name='vehiculo'),
]


# url de guardar el registro de un vehiculo
urlpatterns += [
    url(r'^add/vehiculo/$', views.VehiculoAdd.as_view(), name='add_vehiculo'),
    url(r'^add/cliente/inline/$', views.ClienteSupra.as_view(), name='cliente'),
    url(r'^list/cliente/$', views.ClienteList.as_view(), name='list_cliente')
]
