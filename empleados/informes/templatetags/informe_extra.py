from django import template
from gpcharts import figure
from django.db import connection
from django.utils.safestring import mark_safe
import datetime
import time
register = template.Library()


@register.filter(name='intcommat')
def intcommat(value):
    return value + 1


@register.filter(name='comision')
def comision(l):
    total = 0
    for x in l:
        total += float(x[5])
    # end for
    return total
# end def


@register.filter(name='valor')
def valor(l, num):
    total = 0
    for x in l:
        total += float(x[num])
    # end for
    return total
# end def


@register.filter(name='cabecera')
def cabecera(x):
    print "*******************************************"
    cursor = connection.cursor()
    cursor.execute('select nombre from operacion_tiposervicio order by id asc;')
    row = cursor.fetchall()
    res = ""
    for q in row:
        res += '<th> %s </th>' % (q[0])
    # end if
    return mark_safe(res)
# end def


def get_minute(f):
    fmt = '%Y-%m-%d %H:%M:%S.%f'
    d1 = datetime.strptime(f, fmt)
    return time.mktime(d1.timetuple())
# end def


@register.filter(name='cuerpo')
def cuerpo(x):
    print x[0]
    sql = 'select  tip_ser.id, tip_ser.nombre,case when ser.estado is null or ser.estado=0 then 0 else 1 end as estado ,case when ser.inicio is null then \'----/--/--\' else ser.inicio end as inicio,case when ser.fin is null then \'----/--/--\' else ser.fin end as fin  from operacion_orden as orden  cross join operacion_tiposervicio as tip_ser left join operacion_servicio as ser on (orden.id=ser.orden_id and tip_ser.id=ser.tipo_id and ser.status=1)  where orden.id = %d   order by tip_ser.id asc;' % (x[0])
    cursor = connection.cursor()
    cursor.execute(sql)
    row = cursor.fetchall()
    print row
    res = ""
    for q in row:
        if q[2] == 1:
            res += '<th> %d </th>' % (get_minute(q[4])-get_minute(q[3]))
        else:
            res += '<th> %s </th>' % (q[4])
        # end if
    # end if
    return mark_safe(res)
# end def***datetime.datetime.strptime(q[4], "%Y-%m-%d %H:%M:%S.%f")

register.inclusion_tag(intcommat)
register.inclusion_tag(comision)
register.inclusion_tag(valor)
register.inclusion_tag(cabecera)
register.inclusion_tag(cuerpo)
