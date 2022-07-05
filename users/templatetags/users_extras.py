from django import template

register = template.Library()


@register.filter
def default_if_zero(distance, value):
    if distance == 0 or distance is None:
        return value
    else:
        return distance
