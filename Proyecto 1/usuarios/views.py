from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Usuario, PerfilUsuario, Notificacion, ActividadUsuario
from django.contrib.auth.forms import UserChangeForm
from django import forms
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth import login, logout
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp import devices_for_user
import qrcode
import qrcode.image.svg
from io import BytesIO
import base64

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada exitosamente para {username}!')
            return redirect('usuarios:login')
    else:
        form = UserCreationForm()
    return render(request, 'usuarios/register.html', {'form': form})

class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['telefono', 'direccion', 'fecha_nacimiento', 'avatar', 'biografia']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email']

@login_required
def notificaciones(request):
    notificaciones = request.user.notificaciones.all()
    return render(request, 'usuarios/notificaciones.html', {
        'notificaciones': notificaciones
    })

@login_required
def marcar_notificacion_leida(request, notificacion_id):
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, usuario=request.user)
    notificacion.marcar_como_leida()
    return JsonResponse({'status': 'success'})

@login_required
def actividades(request):
    actividades = request.user.actividades.all()
    return render(request, 'usuarios/actividades.html', {
        'actividades': actividades
    })

def registrar_actividad(usuario, tipo, descripcion, request=None):
    ActividadUsuario.objects.create(
        usuario=usuario,
        tipo=tipo,
        descripcion=descripcion,
        ip_address=request.META.get('REMOTE_ADDR') if request else None
    )

@login_required
def perfil(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        perfil_form = PerfilUsuarioForm(request.POST, request.FILES, instance=request.user.perfilusuario)
        
        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            registrar_actividad(
                request.user,
                'perfil_actualizado',
                'Perfil actualizado exitosamente',
                request
            )
            messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
            return redirect('usuarios:perfil')
    else:
        user_form = UserForm(instance=request.user)
        perfil_form = PerfilUsuarioForm(instance=request.user.perfilusuario)
    
    return render(request, 'usuarios/perfil.html', {
        'user_form': user_form,
        'perfil_form': perfil_form
    })

@login_required
def configurar_2fa(request):
    # Obtener o crear el dispositivo TOTP
    device, created = TOTPDevice.objects.get_or_create(user=request.user, defaults={'name': 'default'})
    
    if request.method == 'POST':
        if 'confirmar' in request.POST:
            token = request.POST.get('token')
            if device.verify_token(token):
                device.confirmed = True
                device.save()
                registrar_actividad(
                    request.user,
                    '2fa_activado',
                    'Autenticación de dos factores activada',
                    request
                )
                messages.success(request, 'La autenticación de dos factores ha sido activada exitosamente.')
                return redirect('usuarios:perfil')
            else:
                messages.error(request, 'Código inválido. Por favor, intenta de nuevo.')
    
    # Generar QR code
    if not device.confirmed:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(device.config_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        qr_code = base64.b64encode(buffer.getvalue()).decode()
    else:
        qr_code = None
    
    return render(request, 'usuarios/configurar_2fa.html', {
        'device': device,
        'qr_code': qr_code
    })

@login_required
def desactivar_2fa(request):
    if request.method == 'POST':
        device = get_object_or_404(TOTPDevice, user=request.user)
        token = request.POST.get('token')
        
        if device.verify_token(token):
            device.delete()
            registrar_actividad(
                request.user,
                '2fa_desactivado',
                'Autenticación de dos factores desactivada',
                request
            )
            messages.success(request, 'La autenticación de dos factores ha sido desactivada exitosamente.')
            return redirect('usuarios:perfil')
        else:
            messages.error(request, 'Código inválido. Por favor, intenta de nuevo.')
    
    return render(request, 'usuarios/desactivar_2fa.html')

def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = Usuario.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Recuperación de contraseña - AutoX"
                    email_template_name = "usuarios/password_reset_email.html"
                    c = {
                        "email": user.email,
                        'domain': request.META['HTTP_HOST'],
                        'site_name': 'AutoX',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https' if request.is_secure() else 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
                        messages.success(request, 'Se ha enviado un correo con instrucciones para recuperar tu contraseña.')
                        return redirect('usuarios:login')
                    except Exception as e:
                        messages.error(request, 'Hubo un error al enviar el correo. Por favor, intenta de nuevo.')
                        return redirect('usuarios:password_reset')
            else:
                messages.error(request, 'No existe una cuenta con ese correo electrónico.')
    else:
        form = PasswordResetForm()
    return render(request, "usuarios/password_reset.html", {"form": form})

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Usuario.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Tu contraseña ha sido restablecida exitosamente.')
                return redirect('usuarios:login')
        else:
            form = SetPasswordForm(user)
        return render(request, 'usuarios/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'El enlace de recuperación de contraseña es inválido o ha expirado.')
        return redirect('usuarios:password_reset')
