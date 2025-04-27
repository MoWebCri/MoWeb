from django import forms
from .models import MensajeContacto

class ContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'asunto', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'asunto': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('', 'Selecciona un asunto'),
                ('cotizacion', 'Solicitud de Cotización'),
                ('proyecto', 'Nuevo Proyecto'),
                ('soporte', 'Soporte Técnico'),
                ('otro', 'Otro')
            ]),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
        } 