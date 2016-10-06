from django.conf.urls import url
import views

# url de tipo de vehiculos
urlpatterns = [
    url(r'^tipo/vehiculo/$', views.TiposVehiculos.as_view(), name='tipo_vehiculo'),
    url(r'^vehiculo/$', views.VehiculoInfo.as_view(), name='vehiculo'),
]
