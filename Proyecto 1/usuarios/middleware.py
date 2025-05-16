from django.core.cache import cache
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

class LoginAttemptsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == reverse('usuarios:login') and request.method == 'POST':
            ip = self.get_client_ip(request)
            cache_key = f'login_attempts_{ip}'
            attempts = cache.get(cache_key, 0)
            
            if attempts >= settings.LOGIN_ATTEMPTS_LIMIT:
                messages.error(request, 'Demasiados intentos fallidos. Por favor, espera 5 minutos antes de intentar nuevamente.')
                return redirect('usuarios:login')
            
            cache.set(cache_key, attempts + 1, settings.LOGIN_ATTEMPTS_TIMEOUT)
        
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip 