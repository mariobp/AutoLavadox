from django import template
from gpcharts import figure
from django.db import connection
from django.utils.safestring import mark_safe
import datetime
import time
register = template.Library()

@register.filter(name='split_valor')
def split_valor(num):
    print 'valor q llego para corte es ',num
    return str(num).split(',')[0]
# end def


register.inclusion_tag(split_valor)
