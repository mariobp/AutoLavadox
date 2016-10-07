from django import forms
import models
from django_select2.forms import (
    HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
    ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
    Select2Widget
)


class AddVehivuloForm(forms.ModelForm):
    class Meta:
        model = models.Vehiculo
        fields = ['placa', 'tipo', ]
        exclude = ['cliente', ]
    # end class
# end class


class AddVehivuloFormAdmin(forms.ModelForm):
    class Meta:
        model = models.Vehiculo
        fields = ['placa', 'tipo', 'cliente']
        exclude = []
        widgets = {
            'tipo': Select2Widget,
            'cliente': Select2Widget
        }
    # end class
# end class
