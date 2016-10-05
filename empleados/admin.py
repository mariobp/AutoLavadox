from django.contrib import admin
from exileui.admin import exileui, ExStacked, ExTabular, DateRangeEX
import models


# Register your models here.
exileui.register(models.Empleado)
