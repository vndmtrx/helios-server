import pytz
from django import template
from django.utils import timezone

register = template.Library()

@register.filter(name='para_gmt3')
def para_gmt3(value):
    if value:
        local_tz = pytz.timezone('America/Sao_Paulo')
        utc_value = timezone.make_aware(value, timezone.utc) if timezone.is_naive(value) else value
        return utc_value.astimezone(local_tz)
    return value