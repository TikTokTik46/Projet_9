from django import template

register = template.Library()

@register.filter
def format_date(value):
    return value.strftime("%H:%M, %d %B %Y")
