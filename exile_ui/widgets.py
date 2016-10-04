from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from django.forms import ModelForm
from sorl.thumbnail import get_thumbnail
from django.template.loader import render_to_string


class DatePickerWidget(forms.DateInput):

    class Media:
        css = {
            'all': ('admin/css/bootstrap.css',)
        }
        js = ('admin/js/jquery-2.2.3.min.js',
              'admin/js/zebra_datepicker.js',
              'admin/js/datepicker.js')
    # end class
# end class


class AdminImageWidget(AdminFileWidget):

    def render(self, name, value, attrs=None):
        output = []
        if value and getattr(value, "url", None):
            t = get_thumbnail(value, '120x120')
            output.append('<img class="form-cicle" src="{}">'.format(t.url))
            output.append(
                super(AdminFileWidget, self).render(name, value, attrs))
            return mark_safe(u''.join(output))
        # end if
        return super(AdminFileWidget, self).render(name, value, attrs)
    # end def
# end class


class MapWidget(forms.Widget):

    def __init__(self, gps1, gps2, attrs=None):
        super(MapWidget, self).__init__(attrs)
        self.gps1 = gps1
        self.gps2 = gps2
    # end def

    def render(self, name, value, attrs=None):
        return render_to_string("reportes/map.html", {'name': name, 'value': value, 'gps1': self.gps1, 'gps2': self.gps2})
    # end def

# end class
