# -*- coding: utf-8 -*-
from django import forms
import models
from django_select2.forms import (
    HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
    ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
    Select2Widget
)


class ServicioForm(forms.ModelForm):
    class Meta:
        model = models.Servicio
        exclude = ()
        fields = {
            'tipo',
            'vehiculo'
        }
        widgets = {
            'tipo': Select2Widget,
            'vehiculo': Select2Widget
        }
    # end class

    def save(self, commit=True):
        servicio = super(ServicioForm, self).save(commit)
        servicio.save()
        print servicio.tipo
        servicio.valor = servicio.tipo.costo
        servicio.comision = servicio.tipo.costo * (servicio.tipo.comision/100)
        servicio.save()
        return servicio
    # end def
# end class
