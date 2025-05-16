from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    TIPO_USUARIO_CHOICES = [
        ('cliente', 'Cliente'),
        ('admin', 'Administrador'),
        ('tecnico', 'Técnico'),
    ]
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES, default='cliente')
    
    # Actualizar related_name para evitar conflictos
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='usuario_set',
        related_query_name='usuario'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='usuario_set',
        related_query_name='usuario'
    )

    def __str__(self):
        return self.username

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    rol = models.CharField(max_length=50, choices=[
        ('admin', 'Administrador'),
        ('vendedor', 'Vendedor'),
        ('tecnico', 'Técnico'),
        ('cliente', 'Cliente')
    ], default='cliente')
    ultima_actividad = models.DateTimeField(auto_now=True)
    biografia = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Perfil de {self.usuario.username}"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(usuario=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def guardar_perfil_usuario(sender, instance, **kwargs):
    instance.perfilusuario.save()

class Notificacion(models.Model):
    TIPOS = [
        ('sistema', 'Sistema'),
        ('inventario', 'Inventario'),
        ('chat', 'Chat'),
        ('perfil', 'Perfil'),
    ]
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificaciones')
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPOS)
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_lectura = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"
    
    def marcar_como_leida(self):
        self.leida = True
        self.fecha_lectura = timezone.now()
        self.save()

class ActividadUsuario(models.Model):
    TIPOS = [
        ('login', 'Inicio de sesión'),
        ('logout', 'Cierre de sesión'),
        ('perfil_actualizado', 'Perfil actualizado'),
        ('inventario_modificado', 'Inventario modificado'),
        ('chat_mensaje', 'Mensaje de chat'),
    ]
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='actividades')
    tipo = models.CharField(max_length=50, choices=TIPOS)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.get_tipo_display()} - {self.fecha}"
