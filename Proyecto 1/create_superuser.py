import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AutoX.settings')
django.setup()

from usuarios.models import Usuario

if not Usuario.objects.filter(username='jose').exists():
    Usuario.objects.create_superuser('jose', 'jose@example.com', 'jose123')
    print('Superusuario creado exitosamente')
else:
    print('El superusuario ya existe') 