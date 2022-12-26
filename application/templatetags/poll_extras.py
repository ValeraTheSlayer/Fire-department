from datetime import datetime, timedelta
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import json

register = template.Library()


@register.filter(expects_localtime=False)
def time_passed(value):
    try:
        return datetime.now() - value > timedelta(hours=1)
    except AttributeError:
        return ''

@register.filter
@stringfilter
def filter_pagination(value, arg):
    try:
        if value.find('page=') != -1:
            return value[:value.find('page=')+5] + str(arg)
        elif '?' in value:
            return value + '&page=' + str(arg)
        else:
            return value + '?&page=' + str(arg)
    except AttributeError:
        return value

@register.filter
@stringfilter
def filter_create_report(value):
    try:
        if value.find('/main_page/') != -1:
            return '/main_page/report-excel/' + value[value.find('/main_page/') + 11:]
        else:
            return '/main_page/report-excel/'
    except AttributeError:
        return value

@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(list(obj)))