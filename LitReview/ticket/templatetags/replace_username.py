from django import template

register = template.Library()


@register.filter
def replace_username(value, user):
    if value == user:
        return "Vous avez"
    else:
        return value+" a"
