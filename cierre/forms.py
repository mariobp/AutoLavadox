from django import forms
import models
from exileui.widgets import DatePickerWidget

class AddTipoServicioForm(forms.ModelForm):
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
        js = ('/static/cierre/js/date.js',)
    # end class

    class Meta:
        model = models.TipoServicio
        fields = ['inicio', 'fin']
        exclude = ['total',]
    # end class
# end class


class AddFacturaForm(forms.ModelForm):
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
        js = ('/static/cierre/js/date.js',)
    # end class

    class Meta:
        model = models.Factura
        fields = ['inicio', 'fin']
        exclude = ['total',]
    # end class
# end class
