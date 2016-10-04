#!/usr/bin/env python
# -*- coding: utf-8 -*-
from import_export.formats import base_formats
import cStringIO as StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
# end def

class PDF(base_formats.Format):

    def get_title(self):
        return 'pdf'
    # end def

    def create_dataset(self, in_stream):
        return list(in_stream)
    # end def

    def export_data(self, dataset, **kwargs):
        return render_to_pdf(
            'informes/informe.html',
            {
                'pagesize': 'A4',
                'dataset': list(dataset),
                'headers': dataset.headers
            }
        )
    # end def

    def is_binary(self):
        return True
    # end def

    def get_read_mode(self):
        return 'rb'
    # end def

    def get_extension(self):
        return "pdf"
    # end def

    def get_content_type(self):
        return 'application/pdf'
    # end def

    def can_import(self):
        return False
    # end def

    def can_export(self):
        return True
    # end def
# end class
