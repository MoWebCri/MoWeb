import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AutoX.settings')
django.setup()

from inventario.models import Categoria

# Lista de categorías a crear
categorias = [
    {
        'nombre': 'Motor',
        'tipo': 'interna',
        'descripcion': 'Piezas y componentes del motor'
    },
    {
        'nombre': 'Transmisión',
        'tipo': 'interna',
        'descripcion': 'Componentes del sistema de transmisión'
    },
    {
        'nombre': 'Frenos',
        'tipo': 'externa',
        'descripcion': 'Sistema de frenos y componentes'
    },
    {
        'nombre': 'Suspensión',
        'tipo': 'externa',
        'descripcion': 'Componentes del sistema de suspensión'
    },
    {
        'nombre': 'Carrocería',
        'tipo': 'externa',
        'descripcion': 'Partes de la carrocería y acabados'
    },
    {
        'nombre': 'Eléctrico',
        'tipo': 'interna',
        'descripcion': 'Componentes del sistema eléctrico'
    }
]

def crear_categorias():
    for cat in categorias:
        Categoria.objects.get_or_create(
            nombre=cat['nombre'],
            defaults={
                'tipo': cat['tipo'],
                'descripcion': cat['descripcion']
            }
        )
        print(f"Categoría '{cat['nombre']}' creada o ya existente")

if __name__ == '__main__':
    print("Creando categorías iniciales...")
    crear_categorias()
    print("Proceso completado!") 