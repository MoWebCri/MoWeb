from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    tipo = forms.ChoiceField(
        choices=[('estudiante', 'Estudiante'), ('docente', 'Docente')],
        label="Tipo de usuario",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2', 'tipo']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar clases de Bootstrap a todos los campos
        for field_name, field in self.fields.items():
            if field_name != 'tipo':  # tipo ya tiene su widget personalizado
                if isinstance(field.widget, forms.PasswordInput):
                    field.widget.attrs.update({'class': 'form-control'})
                else:
                    field.widget.attrs.update({'class': 'form-control'})
        
        # Personalizar mensajes de ayuda
        self.fields['username'].help_text = 'Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.'
        self.fields['password1'].help_text = 'Tu contraseña debe contener al menos 8 caracteres.'
        self.fields['password2'].help_text = 'Ingresa la misma contraseña para verificación.'

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu usuario'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu contraseña'})
    ) 