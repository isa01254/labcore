from django import template

register = template.Library()


@register.filter
def get_item(mapping, key):
    return mapping.get(str(key), 0) if isinstance(mapping, dict) else 0
