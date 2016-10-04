# -*- coding: utf-8 -*-
from django import forms
import models


class ServicioForm(forms.ModelForm):
    class Meta:
        model = models.Servicio
        exclude = ()
        widgets = {
            'vehiculo': SearchableSelect(model='cliente.Vehiculo', search_field='placa')
        }
    # end class
# end class
