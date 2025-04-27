from django.contrib import admin
from .models import MensajeContacto

@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'asunto', 'fecha_envio')
    list_filter = ('fecha_envio', 'asunto')
    search_fields = ('nombre', 'email', 'asunto', 'mensaje')
    readonly_fields = ('fecha_envio',)
    ordering = ('-fecha_envio',)
