from django import template

register = template.Library()

@register.filter
def incrementValue(value, arg):

    value = value + arg
    return value