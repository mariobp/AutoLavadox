# -*- coding: utf-8 -*-
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse

from autolavadox.service import Service


def is_user_redirect_view(function):
    def wrap(request, *args, **kwargs):
        user_id = request.user.id
        servi = Service.get_instance()
        result = servi.isClienteLavadero(user_id)
        if servi.isRecepcionista(user_id) or servi.isClienteLavadero(user_id):
            return function(request, *args, **kwargs)
        elif servi.isCajero(user_id) or servi.isAdministrador(user_id) or request.user.is_superuser:
            return HttpResponseRedirect('/dashboard')
        return HttpResponseRedirect('/dashboard')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap