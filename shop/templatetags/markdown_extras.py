from django import template
from django.utils.safestring import mark_safe
import markdown as md

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    if not text:
        return ""
    # Soporta tablas, listas y bloques de código
    return mark_safe(md.markdown(text, extensions=['tables', 'fenced_code', 'nl2br']))
