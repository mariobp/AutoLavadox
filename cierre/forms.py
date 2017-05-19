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
