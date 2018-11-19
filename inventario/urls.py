from django.conf.urls import url
import views


# url ws de tipo de servicios porvehiculo
urlpatterns = [
    url(r'^cierre/(?P<pk>\d+)/$', views.CierreView.as_view(), name='cierre'),
]
