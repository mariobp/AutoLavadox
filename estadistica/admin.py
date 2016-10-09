from django.contrib import admin
from exileui.admin import exileui, ExStacked, ExTabular, DateRangeEX
import models


class TiemposOrdenAdmin(admin.ModelAdmin):
    list_display = ['orden', 'inicio', 'fin']
    list_filter = ['orden', 'inicio', 'fin']
    search_fields = list_filter
# end class

exileui.register(models.TiemposOrden, TiemposOrdenAdmin)
