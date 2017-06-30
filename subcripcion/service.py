#!/usr/bin/python
# -*- coding: utf-8 -*-
#import models
from usuarios import models as usuario
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
"""
    @classmethod
    def isCliente(sef, request):
        empleado = usuario.Cliente.objects.filter(id=CuserMiddleware.get_user().id)
        if empleado:
            return True,empleado
        #end if
        return False,None
    #end def

    @classmethod
    def isEmpeado(sef, request):
        empleado = usuario.Empleado.objects.filter(cuenta__suscripcion__activa=True, cuenta__suscripcion__factura__paga=True,id=CuserMiddleware.get_user().id)
        if empleado:
            return True,empleado
        #end if
        return False,None
    #end def

    @classmethod
    def isAsistente(sef, request):
        asistente = usuario.Asistente.objects.filter(cuenta__suscripcion__activa=True, cuenta__suscripcion__factura__paga=True,id=CuserMiddleware.get_user().id)
        if asistente :
            return True, asistente
        #end if
        return False, None
    #end def
"""
    @classmethod
    def getCuenta(self, request):
        cuenta = models.Cuenta.objects.filter(Q(cliente__id=request.user.id)).first()
    #end def

    @classmethod
    def isGerente(sef, request):
        return 'el man es gerente'
    #end def
#end class
"""
def main():
    servicio = Service.get_instance()
    print servicio.isCliente(12)
    print 'jajajaja'
# end def

# test de la clase
main()
""""
