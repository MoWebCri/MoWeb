DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configuración de correo
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'cristian.urrutia.alvarez.20@gmail.com'
EMAIL_HOST_PASSWORD = 'tu_contraseña_de_aplicación'  # Debes generar una contraseña de aplicación en Gmail 