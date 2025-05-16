from django.contrib import admin
from .models import MensajeContacto

@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'leido', 'fecha')
    list_filter = ('leido', 'fecha')
    search_fields = ('nombre', 'email', 'mensaje')
    ordering = ('-fecha',)
    readonly_fields = ('fecha',)
    actions = ['marcar_como_leido', 'marcar_como_no_leido']
    
    def marcar_como_leido(self, request, queryset):
        queryset.update(leido=True)
    marcar_como_leido.short_description = "Marcar mensajes seleccionados como leídos"
    
    def marcar_como_no_leido(self, request, queryset):
        queryset.update(leido=False)
    marcar_como_no_leido.short_description = "Marcar mensajes seleccionados como no leídos"
