import pytz
from django.utils import timezone

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define o fuso horário desejado (GMT-3)
        timezone.activate(pytz.timezone('America/Sao_Paulo'))
        response = self.get_response(request)
        timezone.deactivate()
        return response