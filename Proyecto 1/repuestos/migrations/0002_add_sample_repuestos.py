from django.db import migrations

def crear_repuestos(apps, schema_editor):
    Categoria = apps.get_model('repuestos', 'Categoria')
    Repuesto = apps.get_model('repuestos', 'Repuesto')
    
    # Crear categorías
    categorias = {
        'filtros': Categoria.objects.create(nombre='Filtros', descripcion='Filtros para vehículos'),
        'frenos': Categoria.objects.create(nombre='Frenos', descripcion='Sistema de frenos'),
        'motor': Categoria.objects.create(nombre='Motor', descripcion='Componentes del motor'),
        'suspension': Categoria.objects.create(nombre='Suspensión', descripcion='Sistema de suspensión'),
    }
    
    # Lista de repuestos por marca
    repuestos_data = {
        'Toyota': [
            {
                'nombre': 'Filtro de aceite Toyota',
                'marca': 'Toyota',
                'modelo_auto': 'Corolla',
                'precio': 15.99,
                'stock': 50,
                'categoria': categorias['filtros'],
                'descripcion': 'Filtro de aceite de alta calidad para Toyota Corolla'
            },
            {
                'nombre': 'Pastillas de freno Toyota',
                'marca': 'Toyota',
                'modelo_auto': 'Corolla',
                'precio': 45.99,
                'stock': 30,
                'categoria': categorias['frenos'],
                'descripcion': 'Pastillas de freno premium para Toyota Corolla'
            },
            {
                'nombre': 'Bujías Toyota',
                'marca': 'Toyota',
                'modelo_auto': 'Corolla',
                'precio': 8.99,
                'stock': 100,
                'categoria': categorias['motor'],
                'descripcion': 'Bujías de iridio para Toyota Corolla'
            },
            {
                'nombre': 'Correa de distribución Toyota',
                'marca': 'Toyota',
                'modelo_auto': 'Corolla',
                'precio': 89.99,
                'stock': 15,
                'categoria': categorias['motor'],
                'descripcion': 'Correa de distribución original Toyota'
            },
            {
                'nombre': 'Amortiguadores Toyota',
                'marca': 'Toyota',
                'modelo_auto': 'Corolla',
                'precio': 129.99,
                'stock': 20,
                'categoria': categorias['suspension'],
                'descripcion': 'Amortiguadores de gas para Toyota Corolla'
            }
        ],
        'Honda': [
            {
                'nombre': 'Filtro de aceite Honda',
                'marca': 'Honda',
                'modelo_auto': 'Civic',
                'precio': 16.99,
                'stock': 45,
                'categoria': categorias['filtros'],
                'descripcion': 'Filtro de aceite de alta calidad para Honda Civic'
            },
            {
                'nombre': 'Pastillas de freno Honda',
                'marca': 'Honda',
                'modelo_auto': 'Civic',
                'precio': 42.99,
                'stock': 35,
                'categoria': categorias['frenos'],
                'descripcion': 'Pastillas de freno premium para Honda Civic'
            },
            {
                'nombre': 'Bujías Honda',
                'marca': 'Honda',
                'modelo_auto': 'Civic',
                'precio': 9.99,
                'stock': 90,
                'categoria': categorias['motor'],
                'descripcion': 'Bujías de iridio para Honda Civic'
            },
            {
                'nombre': 'Correa de distribución Honda',
                'marca': 'Honda',
                'modelo_auto': 'Civic',
                'precio': 92.99,
                'stock': 12,
                'categoria': categorias['motor'],
                'descripcion': 'Correa de distribución original Honda'
            },
            {
                'nombre': 'Amortiguadores Honda',
                'marca': 'Honda',
                'modelo_auto': 'Civic',
                'precio': 134.99,
                'stock': 18,
                'categoria': categorias['suspension'],
                'descripcion': 'Amortiguadores de gas para Honda Civic'
            }
        ],
        'Ford': [
            {
                'nombre': 'Filtro de aceite Ford',
                'marca': 'Ford',
                'modelo_auto': 'Focus',
                'precio': 14.99,
                'stock': 55,
                'categoria': categorias['filtros'],
                'descripcion': 'Filtro de aceite de alta calidad para Ford Focus'
            },
            {
                'nombre': 'Pastillas de freno Ford',
                'marca': 'Ford',
                'modelo_auto': 'Focus',
                'precio': 39.99,
                'stock': 40,
                'categoria': categorias['frenos'],
                'descripcion': 'Pastillas de freno premium para Ford Focus'
            },
            {
                'nombre': 'Bujías Ford',
                'marca': 'Ford',
                'modelo_auto': 'Focus',
                'precio': 7.99,
                'stock': 110,
                'categoria': categorias['motor'],
                'descripcion': 'Bujías de iridio para Ford Focus'
            },
            {
                'nombre': 'Correa de distribución Ford',
                'marca': 'Ford',
                'modelo_auto': 'Focus',
                'precio': 85.99,
                'stock': 14,
                'categoria': categorias['motor'],
                'descripcion': 'Correa de distribución original Ford'
            },
            {
                'nombre': 'Amortiguadores Ford',
                'marca': 'Ford',
                'modelo_auto': 'Focus',
                'precio': 124.99,
                'stock': 22,
                'categoria': categorias['suspension'],
                'descripcion': 'Amortiguadores de gas para Ford Focus'
            }
        ],
        'Chevrolet': [
            {
                'nombre': 'Filtro de aceite Chevrolet',
                'marca': 'Chevrolet',
                'modelo_auto': 'Cruze',
                'precio': 15.49,
                'stock': 48,
                'categoria': categorias['filtros'],
                'descripcion': 'Filtro de aceite de alta calidad para Chevrolet Cruze'
            },
            {
                'nombre': 'Pastillas de freno Chevrolet',
                'marca': 'Chevrolet',
                'modelo_auto': 'Cruze',
                'precio': 41.99,
                'stock': 32,
                'categoria': categorias['frenos'],
                'descripcion': 'Pastillas de freno premium para Chevrolet Cruze'
            },
            {
                'nombre': 'Bujías Chevrolet',
                'marca': 'Chevrolet',
                'modelo_auto': 'Cruze',
                'precio': 8.49,
                'stock': 95,
                'categoria': categorias['motor'],
                'descripcion': 'Bujías de iridio para Chevrolet Cruze'
            },
            {
                'nombre': 'Correa de distribución Chevrolet',
                'marca': 'Chevrolet',
                'modelo_auto': 'Cruze',
                'precio': 88.99,
                'stock': 13,
                'categoria': categorias['motor'],
                'descripcion': 'Correa de distribución original Chevrolet'
            },
            {
                'nombre': 'Amortiguadores Chevrolet',
                'marca': 'Chevrolet',
                'modelo_auto': 'Cruze',
                'precio': 127.99,
                'stock': 19,
                'categoria': categorias['suspension'],
                'descripcion': 'Amortiguadores de gas para Chevrolet Cruze'
            }
        ],
        'Volkswagen': [
            {
                'nombre': 'Filtro de aceite Volkswagen',
                'marca': 'Volkswagen',
                'modelo_auto': 'Golf',
                'precio': 16.49,
                'stock': 42,
                'categoria': categorias['filtros'],
                'descripcion': 'Filtro de aceite de alta calidad para Volkswagen Golf'
            },
            {
                'nombre': 'Pastillas de freno Volkswagen',
                'marca': 'Volkswagen',
                'modelo_auto': 'Golf',
                'precio': 44.99,
                'stock': 28,
                'categoria': categorias['frenos'],
                'descripcion': 'Pastillas de freno premium para Volkswagen Golf'
            },
            {
                'nombre': 'Bujías Volkswagen',
                'marca': 'Volkswagen',
                'modelo_auto': 'Golf',
                'precio': 9.49,
                'stock': 85,
                'categoria': categorias['motor'],
                'descripcion': 'Bujías de iridio para Volkswagen Golf'
            },
            {
                'nombre': 'Correa de distribución Volkswagen',
                'marca': 'Volkswagen',
                'modelo_auto': 'Golf',
                'precio': 91.99,
                'stock': 11,
                'categoria': categorias['motor'],
                'descripcion': 'Correa de distribución original Volkswagen'
            },
            {
                'nombre': 'Amortiguadores Volkswagen',
                'marca': 'Volkswagen',
                'modelo_auto': 'Golf',
                'precio': 132.99,
                'stock': 17,
                'categoria': categorias['suspension'],
                'descripcion': 'Amortiguadores de gas para Volkswagen Golf'
            }
        ]
    }
    
    # Crear los repuestos
    for marca, repuestos in repuestos_data.items():
        for repuesto_data in repuestos:
            Repuesto.objects.create(**repuesto_data)

def eliminar_repuestos(apps, schema_editor):
    Categoria = apps.get_model('repuestos', 'Categoria')
    Categoria.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('repuestos', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(crear_repuestos, eliminar_repuestos),
    ] 