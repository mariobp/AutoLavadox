#!/usr/bin/python
# -*- coding: utf-8 -*-
from subcripcion import models as suscripcion
from cuser.middleware import CuserMiddleware
from django.db.models import Q

class Service():
    instance = None

    @staticmethod
    def get_instance():
        if Service.instance == None:
            Service.instance = Service()
        #end if
        return Service.instance
    #end def

    @classmethod
    def getCuenta(sef):
        user = CuserMiddleware.get_user()
        if user:
            id =CuserMiddleware.get_user().id
            print 'el id del usuario es ',id
            cuenta = suscripcion.Cuenta.objects.filter(Q(cliente__id=id)|Q(persona__id=id)).first()
            return cuenta
        #end if
        return None
    #end def

    @classmethod
    def isUser(sef):
        user = CuserMiddleware.get_user()
        if user:
            id =CuserMiddleware.get_user().id
            cuenta = suscripcion.Cuenta.objects.filter(Q(cliente__id=id)|Q(persona__id=id)).first()
            r_cuenta =  True if cuenta else False
            return r_cuenta,True,user.is_superuser
        #end if
        return False,False
    #end def
#end class
