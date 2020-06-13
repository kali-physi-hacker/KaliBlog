from django import template

register = template.Library()


@register.filter(name="modulo_two")
def modulo_two(num, val):
    return num % val
