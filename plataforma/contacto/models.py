from django.db import models
from django.utils import timezone

# Create your models here.

class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)
    leido = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Mensaje de Contacto'
        verbose_name_plural = 'Mensajes de Contacto'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.nombre} - {self.email}"
