from django.contrib import admin
from .models import ChatMensaje

@admin.register(ChatMensaje)
class ChatMensajeAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'mensaje', 'fecha')
    list_filter = ('usuario', 'fecha')
    search_fields = ('mensaje',)
    date_hierarchy = 'fecha' 