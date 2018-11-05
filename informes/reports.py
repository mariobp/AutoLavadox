#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @author: Exile
    @date: 05-07-2016
    @place: Cartagena - Colombia
    @licence: Creative Common
"""
from django.contrib import admin
from exileui.admin import exileui
from import_export.formats import base_formats
from import_export.admin import ExportMixin, ImportExportModelAdmin
from import_export import resources, fields
from plugins.pdf.format import PDF


class PdfExportMixin(ExportMixin):

    def get_export_formats(self,):
        formats = super(PdfExportMixin, self).get_export_formats()
        if self.template:
            PDF.template = self.template
        # end if
        return [base_formats.CSV, base_formats.XLSX]
    # end def
# end class


registry = {}

def register_export(model, resource_class, template=None):
	registry[model] = resource_class, template
# end def

old_register = exileui.register

def register(model, *args):
    if model in registry:
    	if len(args):
    		modeladmin = args[0]
    	else:
    		modeladmin = admin.ModelAdmin
    	# end if
        resource_class, template = registry[model]
        class newadmin(PdfExportMixin, modeladmin):
            pass
        # end class
        newadmin.template = template
        newadmin.resource_class = resource_class
        return old_register(model, newadmin)
    # end if
    return old_register(model, *args)
# end def


exileui.register = register
