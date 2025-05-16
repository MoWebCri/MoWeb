from django.contrib import admin
from .models import Categoria, Repuesto, Carrito

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Repuesto)
class RepuestoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'modelo_auto', 'año_auto', 'categoria', 'precio', 'stock')
    list_filter = ('categoria', 'marca', 'modelo_auto')
    search_fields = ('nombre', 'marca', 'modelo_auto', 'año_auto')
    list_editable = ('stock', 'precio')
    ordering = ('nombre',)

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'repuesto', 'cantidad', 'fecha_agregado')
    list_filter = ('usuario', 'fecha_agregado')
    search_fields = ('usuario__username', 'repuesto__nombre')
