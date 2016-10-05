from django.contrib import admin
from exileui.admin import exileui, ExStacked, ExTabular, DateRangeEX
import models
import nested_admin
import forms


class OperarioAdmin(nested_admin.NestedModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'direccion', 'telefono', 'nacimiento')
    search_fields = list_display
    form = forms.OperarioForm

    def get_form(self, request, obj=None, *args, **kwargs):
        if obj:
            kwargs['form'] = forms.OperarioFormEdit
        # end if
        return super(OperarioAdmin, self).get_form(request, obj, *args, **kwargs)
    # end def
# end class


# Register your models here.
exileui.register(models.Empleado, OperarioAdmin)
exileui.register(models.Recepcionista)
exileui.register(models.Cajero)
