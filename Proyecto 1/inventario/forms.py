from django import forms
from .models import Producto, Categoria, Movimiento

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'marca', 'descripcion', 'categoria', 
                 'precio_compra', 'precio_venta', 'stock', 
                 'stock_minimo', 'ubicacion', 'imagen']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'precio_compra': forms.NumberInput(attrs={'step': '0.01'}),
            'precio_venta': forms.NumberInput(attrs={'step': '0.01'}),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'tipo', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['tipo', 'cantidad', 'observacion']
        widgets = {
            'observacion': forms.Textarea(attrs={'rows': 3}),
        } 