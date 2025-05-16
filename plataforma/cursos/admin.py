from django.contrib import admin
from .models import Curso, Carrito, ItemCarrito, Compra, DetalleCompra

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'precio', 'fecha_inicio')
    list_filter = ('categoria', 'fecha_inicio')
    search_fields = ('titulo', 'descripcion')
    ordering = ('-fecha_inicio',)
    readonly_fields = ('fecha_inicio',)
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'descripcion', 'imagen')
        }),
        ('Detalles', {
            'fields': ('precio', 'enlace_moodle', 'categoria')
        }),
        ('Sistema', {
            'fields': ('fecha_inicio',),
            'classes': ('collapse',)
        }),
    )

class ItemCarritoInline(admin.TabularInline):
    model = ItemCarrito
    extra = 0

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_creacion', 'total')
    list_filter = ('fecha_creacion',)
    search_fields = ('usuario__username', 'usuario__email')
    inlines = [ItemCarritoInline]

class DetalleCompraInline(admin.TabularInline):
    model = DetalleCompra
    extra = 0

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_compra', 'estado', 'total')
    list_filter = ('estado', 'fecha_compra')
    search_fields = ('usuario__username', 'usuario__email')
    inlines = [DetalleCompraInline]
