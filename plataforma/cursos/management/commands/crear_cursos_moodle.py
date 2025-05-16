from django.core.management.base import BaseCommand
from django.utils import timezone
from cursos.models import Curso
from datetime import timedelta

class Command(BaseCommand):
    help = 'Crea los cursos de capacitación en Moodle'

    def handle(self, *args, **kwargs):
        cursos_data = [
            {
                'titulo': 'Primeros Pasos en Moodle - Plan Básico',
                'descripcion': 'Curso diseñado para docentes o administradores que recién comienzan con Moodle. '
                             'Aprenderás los conceptos fundamentales y la navegación básica del entorno.',
                'contenido': '''Día 1: Introducción a Moodle
• ¿Qué es Moodle y para qué sirve?
• Navegación básica del entorno
• Diferencia entre profesor, alumno y administrador
• Acceso a cursos y áreas principales

Día 2: Gestión de Usuarios
• Crear usuarios manualmente
• Asignación de roles: profesor, estudiante, gestor
• Subir imagen y editar perfil
• Eliminar o suspender usuarios

Día 3: Creación y gestión de cursos
• Crear un curso nuevo
• Añadir bloques, secciones y descripciones
• Matriculación manual de estudiantes
• Uso de temas y diseño simple''',
                'precio': 17500,
                'categoria': 'otros',
                'duracion': 3,
                'fecha_inicio': timezone.now() + timedelta(days=7),
                'enlace_moodle': 'https://moodle.ejemplo.com/course/view.php?id=1',
            },
            {
                'titulo': 'Curso Efectivo en Moodle - Plan Intermedio',
                'descripcion': 'Dirigido a docentes que ya crean cursos y desean optimizar el uso de Moodle. '
                             'Aprenderás a utilizar recursos, actividades y evaluaciones de manera efectiva.',
                'contenido': '''Sesión 1: Recursos y Actividades
• Diferencias entre recurso y actividad
• Añadir archivos PDF, enlaces y páginas de texto
• Actividad de tarea y foro
• Configuración básica de cada recurso

Sesión 2: Evaluaciones y Calificaciones
• Crear cuestionarios y preguntas
• Parámetros del cuestionario (tiempo, intentos, retroalimentación)
• Calificar tareas manualmente
• Acceder al libro de calificaciones

Sesión 3: Comunicación y Seguimiento
• Uso de mensajes, avisos y foros
• Seguimiento del progreso de los estudiantes
• Informes básicos
• Uso de insignias y retroalimentación''',
                'precio': 30000,
                'categoria': 'otros',
                'duracion': 6,
                'fecha_inicio': timezone.now() + timedelta(days=14),
                'enlace_moodle': 'https://moodle.ejemplo.com/course/view.php?id=2',
            },
            {
                'titulo': 'Gestión Profesional de Moodle - Plan Avanzado',
                'descripcion': 'Curso avanzado para administradores de plataforma o docentes que buscan '
                             'profundizar en la gestión y personalización de Moodle.',
                'contenido': '''Sesión 1: Configuración de la Plataforma
• Panel de administración
• Ajustes generales, idioma, calendario, zona horaria
• Crear categorías y subcategorías

Sesión 2: Usuarios a Nivel Avanzado
• Subida masiva de usuarios desde CSV
• Matriculación automática
• Restricciones de acceso y grupos

Sesión 3: Personalización
• Editar temas y plantillas
• Agregar logos, colores institucionales
• Bloques personalizados y HTML

Sesión 4: Seguridad y Copias de Seguridad
• Roles personalizados
• Permisos por rol
• Crear y restaurar respaldos

Sesión 5: Integraciones
• Plugins esenciales para evaluaciones, informes, gamificación
• Moodle Mobile (uso desde dispositivos móviles)
• Integración con plataformas externas (Google, Microsoft)''',
                'precio': 50000,
                'categoria': 'otros',
                'duracion': 10,
                'fecha_inicio': timezone.now() + timedelta(days=21),
                'enlace_moodle': 'https://moodle.ejemplo.com/course/view.php?id=3',
            },
            {
                'titulo': 'Moodle para Empresas - Plan Personalizado',
                'descripcion': 'Curso especializado para empresas que necesitan implementar Moodle '
                             'con certificación SENCE y reportes específicos.',
                'contenido': '''Contenido Personalizado:
• Manejo de tokens SENCE
• Creación de cursos certificados
• Reportes específicos para entidades externas
• Moodle adaptado a empresas (empleados vs. estudiantes)

El contenido específico se adaptará según las necesidades de tu empresa.''',
                'precio': 300000,
                'categoria': 'otros',
                'duracion': 15,
                'fecha_inicio': timezone.now() + timedelta(days=30),
                'enlace_moodle': 'https://moodle.ejemplo.com/course/view.php?id=4',
            }
        ]

        for curso_data in cursos_data:
            curso, created = Curso.objects.get_or_create(
                titulo=curso_data['titulo'],
                defaults=curso_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Curso creado exitosamente: {curso.titulo}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'El curso ya existe: {curso.titulo}')
                ) 