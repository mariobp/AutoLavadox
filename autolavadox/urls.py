
"""autolavadox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from exileui.admin import exileui
import settings
from django.views.generic.base import RedirectView
from empleados import views as empleado
favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    url(r'^dashboard/logout/$', empleado.Logout.as_view()),
    url(r'^dashboard/login/$', empleado.Login.as_view()),    
    url(r'^dashboard/', exileui.urls),
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^', include('interface.urls')),
    url(r'^empleados/', include('empleados.urls', namespace='empleado')),
    url(r'^cliente/', include('cliente.urls', namespace='cliente')),
    url(r'^operacion/', include('operacion.urls', namespace='operacion')),
    url(r'^cierre/', include('cierre.urls', namespace='cierre')),
    url(r'^favicon\.ico$', favicon_view),
]
"""
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)"""
