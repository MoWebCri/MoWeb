import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AutoX.settings')
django.setup()

from repuestos.models import Categoria, Repuesto
from django.contrib.auth.models import User

def crear_datos_ejemplo():
    # Crear categorías
    categorias = [
        {
            'nombre': 'Motor',
            'descripcion': 'Repuestos para el motor del vehículo'
        },
        {
            'nombre': 'Frenos',
            'descripcion': 'Sistema de frenos y componentes relacionados'
        },
        {
            'nombre': 'Suspensión',
            'descripcion': 'Componentes del sistema de suspensión'
        },
        {
            'nombre': 'Eléctrico',
            'descripcion': 'Componentes eléctricos y electrónicos'
        }
    ]

    for cat_data in categorias:
        Categoria.objects.get_or_create(
            nombre=cat_data['nombre'],
            defaults={'descripcion': cat_data['descripcion']}
        )

    # Crear repuestos
    repuestos = [
        {
            'nombre': 'Filtro de Aceite',
            'descripcion': 'Filtro de aceite de alta calidad para motor',
            'precio': 15.99,
            'stock': 50,
            'categoria': 'Motor'
        },
        {
            'nombre': 'Pastillas de Freno',
            'descripcion': 'Pastillas de freno cerámicas',
            'precio': 45.99,
            'stock': 30,
            'categoria': 'Frenos'
        },
        {
            'nombre': 'Amortiguadores',
            'descripcion': 'Par de amortiguadores delanteros',
            'precio': 89.99,
            'stock': 20,
            'categoria': 'Suspensión'
        },
        {
            'nombre': 'Batería',
            'descripcion': 'Batería de 12V 60Ah',
            'precio': 120.99,
            'stock': 15,
            'categoria': 'Eléctrico'
        }
    ]

    for rep_data in repuestos:
        categoria = Categoria.objects.get(nombre=rep_data['categoria'])
        Repuesto.objects.get_or_create(
            nombre=rep_data['nombre'],
            defaults={
                'descripcion': rep_data['descripcion'],
                'precio': rep_data['precio'],
                'stock': rep_data['stock'],
                'categoria': categoria
            }
        )

if __name__ == '__main__':
    print('Creando datos de ejemplo...')
    crear_datos_ejemplo()
    print('¡Datos de ejemplo creados exitosamente!') 