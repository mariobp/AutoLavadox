from django.conf.urls import url
import views


# url ws de tipo de vehiculos
urlpatterns = [
    url(r'^ws/tipo/vehiculo/$', views.TiposServicios.as_view(), name='ws_tipo_vehiculo'),
]
