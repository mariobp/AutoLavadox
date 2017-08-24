# -*- coding: utf-8 -*-
from django import forms
import models
from exileui.widgets import DatePickerWidget
from autolavadox import service
from django.db.models import Q


class BaseForm(forms.ModelForm):
    def save(self, commit=True):
        data = super(BaseForm, self).save(commit)
        data.save()
        ser = service.Service.get_instance()
        tem_cuenta,is_user,admin = ser.isUser()
        if tem_cuenta and is_user :
            cuenta = ser.getCuenta()
            data.cuenta = cuenta
        elif admin:
            print 'Es un super usuario'
        #end if
        data.save()
        return data
    #end def
#end class

class AddTipoServicioForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(AddTipoServicioForm, self).__init__(*args, **kwargs)
        self.fields['inicio'].widget = DatePickerWidget(
            attrs={'class': 'datecierre'},
            format="%d/%m/%Y")
        self.fields['fin'].widget = DatePickerWidget(
            attrs={'class': 'datecierre'},
            format="%d/%m/%Y")
    # end def

    def clean(self):
        data = super(AddTipoServicioForm, self).clean()
        print data,data.get('fin')
        if not data.get('fin') :
            self.add_error('fin', 'Debe digitar la fecha de fin de reporte')
        # end if
        if not data.get('inicio') :
            self.add_error('fin', 'Debe digitar la fecha de fin de reporte')
        # end if
        if data.get('fin')   and data.get('inicio')  :
            if data.get('fin') < data.get('inicio') :
                self.add_error('inicio', 'La fecha de inio debe ser menor a la de fin')
            # end if
        #end if
    # end def

    class Media:
        js = ('https://storage.googleapis.com/autolavadox/static/cierre/js/date.js',)
    # end class

    class Meta:
        model = models.TipoServicio
        fields = ['inicio', 'fin']
        exclude = ['total',]
    # end class
# end class


class AddFacturaForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(AddTipoServicioForm, self).__init__(*args, **kwargs)
        self.fields['inicio'].widget = DatePickerWidget(
            attrs={'class': 'datecierre'},
            format="%d/%m/%Y")
        self.fields['fin'].widget = DatePickerWidget(
            attrs={'class': 'datecierre'},
            format="%d/%m/%Y")
    # end def

    class Media:
        js = ('https://storage.googleapis.com/autolavadox/static/cierre/js/date.js',)
    # end class

    class Meta:
        model = models.Factura
        fields = ['inicio', 'fin']
        exclude = ['total',]
    # end class

    def clean(self):
        data = super(AddFacturaForm, self).clean()
        if not data.get('fin') :
            self.add_error('fin', 'Debe digitar la fecha de fin de reporte')
        # end if
        if not data.get('inicio') :
            self.add_error('fin', 'Debe digitar la fecha de fin de reporte')
        # end if
        if data.get('fin') and data.get('inicio'):
            if data.get('fin') < data.get('inicio') :
                self.add_error('inicio', 'La fecha de inio debe ser menor a la de fin')
            # end if
        #end if
    # end def
# end class
