from django.template import Library
from django.conf import settings
import json as parse_json
from exile_ui.admin import admin_site, ExTabular, ExStacked
import operator
register = Library()


@register.filter(name='is_exinline')
def is_exinline(obj):
    print type(obj.opts).__bases__
    bases = type(obj.opts).__bases__
    return ExTabular in bases or ExStacked in bases
# end def


@register.filter(name='exsub')
def exsub(arr, key):
    if arr and key:
        return arr.get(key)
    # end if
    return None
# end def


@register.assignment_tag(name='extest')
def extest(arr=None, **kwargs):
    if not arr or not isinstance(arr, list):
        arr = []
    # end if
    if bool(kwargs):
        name = kwargs['name']
        link = kwargs['link']
        arr.append({'name': name, 'link': link})
    # end if
    return arr
# end def


@register.filter(name='exgetlast')
def exgetlast(arr):
    if isinstance(arr, list):
        return arr[-1]['name']
    # end if
    return None
# end def


def ex_applist_arr_add(arr, group, name, url, icon):
    if not arr.get(group):
        arr[group] = []
    # end if
    arr[group].append({'name': name, 'url': url, 'icon': icon})
# end def


def ex_applist_add(arr, group, model, app_name):
    ex_applist_arr_add(
        arr, group,
        unicode(model['name']),
        model['admin_url'],
        settings.EXILE_UI['media']['icons'][app_name]['models'][model['object_name']]['icon']
    )
# end def


def ex_applist_extra(arr, app_name):
    if settings.EXILE_UI['media']['icons'][app_name].get('menu-extra'):
        for extra in settings.EXILE_UI['media']['icons'][app_name]['menu-extra']:
            if extra.get('group'):
                ex_applist_arr_add(arr, extra['group'], extra['name'], extra['url'], extra['icon'])
            else:
                ex_applist_arr_add(arr, 'Otros', extra['name'], extra['url'], extra['icon'])
            # end if
        # end for
    # end if
# end def


@register.simple_tag
def ex_applist(models, app_name):
    json = {}
    if settings.EXILE_UI['media']['icons'][app_name].get('groups'):
        for group in settings.EXILE_UI['media']['icons'][app_name]['groups']:
            for model in models:
                if group == settings.EXILE_UI['media']['icons'][app_name]['models'][model['object_name']].get('group'):
                    ex_applist_add(json, group, model, app_name)
                # end if
            # end for
        # end for
        for model in models:
            if settings.EXILE_UI['media']['icons'][app_name]['models'][model['object_name']].get('group') is None:
                ex_applist_add(json, 'Otros', model, app_name)
            # end if
        # end for
        ex_applist_extra(json, app_name)
    else:
        for model in models:
            ex_applist_add(json, 'Otros', model, app_name)
        # end for
        ex_applist_extra(json, app_name)
    # end if
    return parse_json.dumps(json)
# end def


@register.simple_tag
def exui():
    return settings.MENU_ORDER
# enddef


@register.assignment_tag
def lm_get(arr=None, key=None, **kwargs):
    if isinstance(arr, list) and key:
        for val in arr:
            if val.get('app_label').lower() == key.lower():
                return val
            # endif
        # endfor
    # endif
    return None
# end def


@register.assignment_tag
def lm_get2(arr=None, key=None, **kwargs):
    if isinstance(arr, list) and key:
        for val in arr:
            if val.get('object_name').lower() == key.lower():
                return val
            # endif
        # endfor
    # endif
    return None
# end def
