from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    TIPO_USUARIO_CHOICES = (
        ('estudiante', 'Estudiante'),
        ('docente', 'Docente'),
    )
    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES, default='estudiante')
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        
    def __str__(self):
        return f"{self.username} - {self.get_tipo_display()}"
    
    @property
    def es_docente(self):
        return self.tipo == 'docente'
    
    @property
    def es_estudiante(self):
        return self.tipo == 'estudiante'
