# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render, redirect
from supra import views as supra
import forms
import models
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from cuser.middleware import CuserMiddleware
from django.views.generic import View, DeleteView
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, get_object_or_404, HttpResponse
from django.views.generic import TemplateView
from django.views.generic.edit import BaseFormView
from django.contrib.auth.views import logout
from django.db.models import Q
# Create your views here.


class ListPlan(supra.SupraListView):
    model = models.Plan
    search_key = 'q'
    list_display = ['id','nombre','descripcion','operadores','asistentes','valor','modulos']
    search_fields = ['id']
    paginate_by = 100

    def modulos(self, obj, row):
        return 'Lunes martes'
    # end def

    def get_queryset(self):
        queryset = super(ListPlan, self).get_queryset()
        user = CuserMiddleware.get_user()
        confi = queryset.filter(estado=True)
        return confi

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ListPlan, self).dispatch(*args, **kwargs)
    # end def
# end class


class AddPlan(supra.SupraFormView):
    model = models.Plan
    form_class = forms.PlanForm
    template_name = 'subcripcion/addplan.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(AddEmpleado, self).dispatch(*args, **kwargs)
    # end def
# end class


class DeletePlan(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(DeletePlan, self).dispatch(*args, **kwargs)
    # end def

    def get(self, request, *args, **kwargs):
        empr=kwargs['pk']
        if empr:
            print 1
            empre = models.Plan.objects.filter(id=empr).first()
            if empre:
                empre.estado=False
                empre.save()
                return HttpResponse('[{"status":true}]', content_type='application/json', status=200)
            # end if
        # end if
        return HttpResponse('[{"status":false}]', content_type='application/json', status=202)
    # end def
# end class


class ListInstModulo(supra.SupraListView):
    model = models.InstModulo
    search_key = 'q'
    list_display = ['id','nombre','descripcion','funcionalidades','estado']
    search_fields = ['plan__id']
    paginate_by = 100

    def funcionalidades(self, obj, row):
        return [{'nombre':x.nombre for x in obj.funcionalidades.all()}]
    # end def

    def get_queryset(self):
        queryset = super(ListItModulo, self).get_queryset()
        instmodulo = queryset.filter(estado=True)
        return instmodulo

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ListItModulo, self).dispatch(*args, **kwargs)
    # end def
# end class


class ListCliente(supra.SupraListView):
    model = models.Cliente
    search_key = 'q'
    list_display = ['id','first_name','last_name','username','telefono','email']
    search_fields = ['id','identificacion']
    paginate_by = 1

    def get_queryset(self):
        queryset = super(ListCliente, self).get_queryset()
        confi = queryset.filter(estado=True)
        return confi
    #end def

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ListCliente, self).dispatch(*args, **kwargs)
    # end def
# end class


class AddCliente(supra.SupraFormView):
    model = models.Cliente
    form_class = forms.ClienteForm
    template_name = 'subcripcion/addcliente.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(AddCliente, self).dispatch(*args, **kwargs)
    # end def
# end class


class EditCliente(supra.SupraFormView):
    model = models.Cliente
    form_class = forms.ClienteEditForm
    template_name = 'subcripcion/addcliente.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(EditCliente, self).dispatch(*args, **kwargs)
    # end def
# end class

class SetPassWordEmpleado(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SetPassWordEmpleado, self).dispatch(request, *args, **kwargs)
    # end def

    def get(self, request, *args, **kwargs):
        return render(request,'subcripcion/setpassword.html')
    #
    def post(self, request, *args, **kwargs):# 359291054481645
        passw = request.GET.get('password',False)
        passw2 = request.GET.get('password2',False)
        if passwo and iden :
            cli = models.Cliente.objects.filter(id=request.user.id).first()
            if cli :
                    cli.set_password(raw_password=password)
                    cli.save()
                    return HttpResponse('{"r":"Ok"}', content_type="application/json", status=200)
            # end if
            return HttpResponse('{"r":"Campos invalidos"}', content_type="application/json", status=400)
        # end if
        return HttpResponse('{"r":"Campos requeridos"}', content_type="application/json", status=400)
    # end def
#end class

class DeleteCliente(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(DeleteCliente, self).dispatch(*args, **kwargs)
    # end def

    def get(self, request, *args, **kwargs):
        empr=kwargs['pk']
        if empr:
            print 1
            empre = models.Cliente.objects.filter(id=empr).first()
            if empre:
                empre.estado=False
                empre.save()
                return HttpResponse('[{"status":true}]', content_type='application/json', status=200)
            # end if
        # end if
        return HttpResponse('[{"status":false}]', content_type='application/json', status=202)
    # end def
# end class


class AddSuscripcion(supra.SupraFormView):
    model = models.Suscripcion
    form_class = forms.SuscripcionForm
    template_name = 'subcripcion/addsuscripcion.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(AddSuscripcion, self).dispatch(*args, **kwargs)
    # end def

    def get_form_kwargs(self):
        kwargs = super(AddSuscripcion, self ).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    #end def
# end class
