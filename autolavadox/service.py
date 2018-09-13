#!/usr/bin/python
# -*- coding: utf-8 -*-
from subcripcion import models as suscripcion
from cuser.middleware import CuserMiddleware
from django.db.models import Q
from empleados import models as empleados

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
    def isRecepcionista(self,id_user):
        user = CuserMiddleware.get_user()
        print 'Valor para el usuario tales ',user
        recepcionista = empleados.Recepcionista.objects.filter(id=id_user)
        print 'esto es lo q hay en recepcionista ',len(recepcionista)
        if recepcionista:
            return True
        #end if
        return False
    #end def

    @classmethod
    def isAdministrador(self,id_user):
        user = CuserMiddleware.get_user()
        administrador = empleados.Administrador.objects.filter(id=id_user).first()
        if administrador:
            return True
        #end if
        return False
    #end def

    @classmethod
    def isCajero(self,id_user):
        user = CuserMiddleware.get_user()
        cajero = empleados.Cajero.objects.filter(id=id_user).first()
        if cajero:
            return True
        #end if
        return False
    #end def

    @classmethod
    def getCuenta(self):
        user = CuserMiddleware.get_user()
        if user:
            id =CuserMiddleware.get_user().id
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

    @classmethod
    def isUserCuenta(sef):
        user = CuserMiddleware.get_user()
        if user:
            id =CuserMiddleware.get_user().id
            cuenta = suscripcion.Cuenta.objects.filter(Q(cliente__id=id)|Q(persona__id=id)).first()
            r_cuenta =  True if cuenta else False
            return r_cuenta
        #end if
        return False
    #end def

    @classmethod
    def getCliente(self):
        user = CuserMiddleware.get_user()
        if user:
            return None
        #end if
        return None
    #end def
#end class
