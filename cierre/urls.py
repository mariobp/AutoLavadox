from django.conf.urls import url
import views


# url ws de tipo de servicios porvehiculo
urlpatterns = [
    url(r'^factura/(?P<pk>\d+)/$', views.Factura.as_view(), name='factura'),
    url(r'^factura/tipo/(?P<pk>\d+)/$', views.FacturaTipo.as_view(), name='factura'),
]
