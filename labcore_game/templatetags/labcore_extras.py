from django import template
register=template.Library()
@register.filter
def get_item(d,k): return d.get(str(k),0) if isinstance(d,dict) else 0