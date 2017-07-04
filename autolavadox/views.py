# -*- coding: utf-8 -*-
from django.contrib import admin
from autolavadox.service import Service


def set_queryset(query):
    ser = Service.get_instance()
    tem_cuenta,is_user,admin = ser.isUser()
    print tem_cuenta,is_user,admin
    print 'esta es una consulta  ',len(query)
    if tem_cuenta and is_user :
        print 'Entro ', ser.getCuenta()
        cuenta = ser.getCuenta()
        query = query.filter(cuenta=cuenta)
        for x in query:
            print x.cuenta.id,'  ',cuenta.id
        #end for
        print len(query.filter(cuenta=cuenta))
    #end if
    print 'esta es una consulta  ',len(query)
    return query
#end def

class BaseAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super(BaseAdmin, self).get_queryset(request)
        queryset= set_queryset(queryset)
        return queryset.filter(Q(status=True)|Q(state=True)).order_by('-id')
    # end def
#end class
