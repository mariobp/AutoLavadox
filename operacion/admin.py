from django.contrib import admin
from exile_ui.admin import admin_site, ExStacked, ExTabular, DateRangeEX
import models
# Register your models here.
admin_site.register(models.TipoServicio)
admin_site.register(models.Servicio)
