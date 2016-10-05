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
        exclude = ('vehiculo',)
        fields = {
            'tipo',
            'empleado'
        }
        widgets = {
            'tipo': Select2Widget,
            'empleado': Select2Widget
        }
    # end class
# end class


class OrdenForm(forms.ModelForm):
    class Meta:
        model = models.Orden
        exclude = ('valor', 'fecha')
        fields = {
            'observacion',
            'vehiculo'
        }
        widgets = {
            'vehiculo': Select2Widget,
            'observacion': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
        }
    # end class

    def save(self, commit=True):
        orden = super(OrdenForm, self).save(commit)
        orden.save()
    # end class
# end class
