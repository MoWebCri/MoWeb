from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactoForm
import json
import time
from datetime import datetime, timedelta

# Diccionario para almacenar los intentos de envío
submission_attempts = {}

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def check_rate_limit(ip_address):
    current_time = datetime.now()
    if ip_address in submission_attempts:
        attempts = submission_attempts[ip_address]
        # Limpiar intentos antiguos (más de 1 hora)
        attempts = [t for t in attempts if current_time - t < timedelta(hours=1)]
        if len(attempts) >= 5:  # Máximo 5 intentos por hora
            return False
        attempts.append(current_time)
        submission_attempts[ip_address] = attempts
    else:
        submission_attempts[ip_address] = [current_time]
    return True

def inicio(request):
    return render(request, 'pag/inicio.html')

def servicios(request):
    return render(request, 'pag/servicios.html')

def sobre_mi(request):
    return render(request, 'pag/sobre_mi.html')

def portafolio(request):
    return render(request, 'pag/portafolio/index.html')

def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            # Guardar el mensaje
            mensaje = form.save()
            
            # Enviar correo al administrador
            asunto_admin = f'Nuevo mensaje de contacto: {mensaje.asunto}'
            mensaje_admin = f'''
            Has recibido un nuevo mensaje de contacto:
            
            Nombre: {mensaje.nombre}
            Email: {mensaje.email}
            Asunto: {mensaje.asunto}
            Mensaje: {mensaje.mensaje}
            '''
            
            send_mail(
                asunto_admin,
                mensaje_admin,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            
            # Enviar correo de confirmación al usuario
            asunto_cliente = 'Gracias por contactarnos - MoWebCri'
            mensaje_cliente = f'''
            Estimado/a {mensaje.nombre},

            Gracias por ponerte en contacto con MoWebCri. Este mensaje es para confirmar que hemos recibido tu consulta correctamente.

            Detalles de tu mensaje:
            Asunto: {mensaje.asunto}
            
            Nos pondremos en contacto contigo lo antes posible para atender tu solicitud. Normalmente respondemos dentro de las próximas 24-48 horas hábiles.

            Si tienes alguna consulta adicional, no dudes en responder a este correo.

            Saludos cordiales,
            Equipo MoWebCri
            '''
            
            send_mail(
                asunto_cliente,
                mensaje_cliente,
                settings.EMAIL_HOST_USER,
                [mensaje.email],
                fail_silently=False,
            )
            
            return render(request, 'pag/contacto.html', {
                'form': ContactoForm(),
                'success': True,
                'mensaje': '¡Gracias por tu mensaje! Te hemos enviado un correo de confirmación.'
            })
    else:
        form = ContactoForm()
    
    return render(request, 'pag/contacto.html', {'form': form})

@csrf_exempt
@require_http_methods(["POST"])
def verify_email(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        # Aquí iría la lógica de verificación de email
        # Por ahora solo simulamos una verificación
        time.sleep(1)  # Simular delay
        return JsonResponse({'valid': True})
    except:
        return JsonResponse({'valid': False}, status=400)


def chat(request):
    return render(request, 'pag/chat.html')

def plantilla_negocio(request):
    return render(request, 'pag/plantillas/negocio.html')

def plantilla_portafolio(request):
    return render(request, 'pag/plantillas/portafolio.html')

def plantilla_elearning(request):
    return render(request, 'pag/plantillas/elearning.html')

def plantilla_repuestos(request):
    return render(request, 'pag/plantillas/pro/repuestos.html')
