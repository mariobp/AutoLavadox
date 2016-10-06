from django import forms
import models


class AddVehivuloForm(forms.ModelForm):
    class Meta:
        model = models.Vehiculo
        fields = ['placa', 'tipo', ]
        exclude = ['cliente', ]
    # end class
# end class
