#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @author: Exile
    @date: 05-07-2016
    @place: Cartagena - Colombia
    @licence: Creative Common
"""
from django.contrib import admin
from exile_ui.admin import admin_site
from import_export.formats import base_formats
from import_export.admin import ExportMixin, ImportExportModelAdmin
from import_export import resources, fields
from plugins.pdf.format import PDF


class PdfExportMixin(ExportMixin):

    def get_export_formats(self,):
        formats = super(PdfExportMixin, self).get_export_formats()
        return [PDF, base_formats.CSV, base_formats.XLSX]
    # end def
# end class


registry = {}

def register_export(model, resource_class):
	registry[model] = resource_class
# end def

old_register = admin_site.register

def register(model, *args):
    if model in registry:
    	if len(args):
    		modeladmin = args[0]
    	else:
    		modeladmin = admin.ModelAdmin
    	# end if
        class newadmin(PdfExportMixin, modeladmin):
            resource_class = registry[model]
        # end class
        return old_register(model, newadmin)
    # end if
    return old_register(model, *args)
# end def


admin_site.register = register
