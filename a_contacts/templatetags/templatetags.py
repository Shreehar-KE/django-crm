from django import template

register = template.Library()


@register.filter
def format_contact_id(value):
    if value < 1000:
        return f"#{value:03d}"
    else:
        return f"#{value}"
