from django.conf.urls import include, url

import views

urlpatterns = [
    url(r'^template/add/$', views.addvehiculo, name="add"),
    url(r'^$', views.index, name="index"),
]
