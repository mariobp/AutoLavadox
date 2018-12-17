from django.conf.urls import url
import views

urlpatterns = [
    url(r'^login/$', views.Login.as_view(), name='user-login'),
    url(r'^logout/$', views.Logout.as_view(), name='user-logout'),
]

# servicio que retorna los Operarios
urlpatterns += [
    url(r'^operarios/$', views.WsOperarios.as_view(), name='operarios'),
    url(r'^operarios/servicio/$', views.WsOperariosServicio.as_view(), name='operarios_servi'),
    url(r'^excel/periodo/$', views.Excel.as_view(), name='operarios'),
    url(r'^excel/empleados/$', views.ExcelEmpleados.as_view(), name='excel_empleados'),
    url(r'^report/comi/$', views.ReporteComisionE.as_view(), name='excel_comision_empleados'),
    url(r'^get/turno/$',views.ConfiguracionTurno.as_view(), name='get_turno'),
]
