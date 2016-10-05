#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @author: Exile
    @date: 05-07-2016
    @place: Cartagena - Colombia
    @licence: Creative Common
"""
import reports
from import_export import resources, widgets, fields
from django.db import models
from django.contrib import admin
from exile_ui.admin import exileui


class ServicioResource(resources.ModelResource):

# end class

reports.register_export(usuarios.Cliente, ClienteResource)
