from django.db import models
from django.conf import settings

class ChatMensaje(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Mensaje de Chat'
        verbose_name_plural = 'Mensajes de Chat'

    def __str__(self):
        return f"{self.usuario.username}: {self.mensaje[:50]}" 