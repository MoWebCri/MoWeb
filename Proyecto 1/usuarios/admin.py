from django.contrib import admin
from .models import Usuario, PerfilUsuario, Notificacion, ActividadUsuario
from django.utils import timezone

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'telefono', 'direccion', 'tipo_usuario', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('tipo_usuario', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'telefono', 'direccion')
    ordering = ('username',)

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'telefono', 'direccion', 'rol', 'ultima_actividad')
    search_fields = ('usuario__username', 'telefono', 'direccion', 'rol')
    list_filter = ('rol',)

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'titulo', 'tipo', 'leida', 'fecha_creacion')
    list_filter = ('tipo', 'leida')
    search_fields = ('usuario__username', 'titulo', 'mensaje')
    ordering = ('-fecha_creacion',)
    actions = ['marcar_como_leidas']

    def marcar_como_leidas(self, request, queryset):
        queryset.update(leida=True, fecha_lectura=timezone.now())
    marcar_como_leidas.short_description = "Marcar notificaciones seleccionadas como leídas"

@admin.register(ActividadUsuario)
class ActividadUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo', 'descripcion', 'fecha', 'ip_address')
    list_filter = ('tipo',)
    search_fields = ('usuario__username', 'descripcion', 'ip_address')
    ordering = ('-fecha',)
