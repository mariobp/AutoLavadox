# -*- coding: utf-8 -*-
from django import forms
import service


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
