from django.contrib import admin
from exileui.admin import exileui, ExStacked, ExTabular, DateRangeEX
import models
from django.utils.html import format_html
import forms
# Register your models here.


class TipoServicioAdmin(admin.ModelAdmin):
    form = forms.AddTipoServicioForm
    list_display = ['id_cierre','inicio','fin','total','accion_reporte']
    list_filter = ['id','inicio','fin',]
    search_fields = ['id','inicio','fin','total']
    list_display_links = ('id_cierre',)

    def id_cierre(self, obj):
        i = 0
        men = ''
        while i < 10 - len(str(obj.pk)):
            men = men + '0'
            i = i+1
        # end ford
        return '%s%d' % (men, obj.pk)
    # end def

    def accion_reporte(self, obj):
        return format_html("<a href='{0}' class='generar addlink'>Imprimir</a>", obj.id)
    # end def

    id_cierre.allow_tags = True
    id_cierre.short_description = 'Cierre Id'
    accion_reporte.allow_tags = True
    accion_reporte.short_description = 'Reporte Dia'
# end class

exileui.register(models.TipoServicio, TipoServicioAdmin)
exileui.register(models.Factura)
