from django.contrib import admin
from exileui.admin import admin_site, ExStacked, ExTabular, DateRangeEX
import models


# Register your models here.
admin_site._registry = admin.site._registry
admin_site.register(models.Empleado)
