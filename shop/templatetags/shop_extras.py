from django import template

register = template.Library()


@register.filter
def surcharge(price, user):
    return price * user.profile.parts_surcharge
