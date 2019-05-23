from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def index(l, i):
    return l[int(i)]

@register.filter
def key(d, key_name):
	return d[key_name]

@register.filter
def get_range(value):
	return range(value)