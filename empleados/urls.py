from django.conf.urls import url
import views

urlpatterns = [
    url(r'^login/', views.Login.as_view(), name='user-login'),
    url(r'^logout/', views.Logout.as_view(), name='user-logout'),
]
