from django import template

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
def valor(l):
    total = 0
    for x in l:
        total += float(x[4])
    # end for
    return total
# end def

register.inclusion_tag(intcommat)
register.inclusion_tag(comision)
register.inclusion_tag(valor)
