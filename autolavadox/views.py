# -*- coding: utf-8 -*-
from django.contrib import admin
from autolavadox.service import Service
from django.db.models import Q
from supra import views as supra


def set_queryset(query):
    ser = Service.get_instance()
    tem_cuenta,is_user,admin = ser.isUser()
    if tem_cuenta and is_user :
        cuenta = ser.getCuenta()
        query = query.filter(cuenta=cuenta)
    #end if
    return query
#end def

def get_cuenta():
    ser = service.Service.get_instance()
    tem_cuenta,is_user,admin = ser.isUser()
    if tem_cuenta :
        cuenta = ser.getCuenta()
        return True,cuenta.id
    else:
        return False,0
    #end if
#end def

class BaseAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super(BaseAdmin, self).get_queryset(request)
        queryset= set_queryset(queryset)
        return queryset.filter(Q(status=True)|Q(state=True)).order_by('-id')
    # end def
#end class

class BaseListSupra(supra.SupraListView):
    def get_queryset(self):
        queryset = super(BaseListSupra, self).get_queryset()
        queryset = set_queryset(queryset)
        return queryset
    # end def
# end class
