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
            'operario'
        }
        widgets = {
            'tipo': Select2Widget,
            'operario': Select2Widget
        }
    # end class
# end class


class OrdenForm(forms.ModelForm):
    class Meta:
        model = models.Orden
        exclude = ('valor',)
        fields = {
            'observacion',
            'vehiculo'
        }
        widgets = {
            'vehiculo': Select2Widget,
            'observacion': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
        }
    # end class
# end class
