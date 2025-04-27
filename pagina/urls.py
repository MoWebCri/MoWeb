from django.urls import path, include
from . import views

urlpatterns = [
    # Páginas principales
    path('', views.inicio, name='inicio'),
    path('servicios/', views.servicios, name='servicios'),
    path('portafolio/', views.portafolio, name='portafolio'),
    path('contacto/', views.contacto, name='contacto'),
    
    # Funcionalidades adicionales
    path('chat/', views.chat, name='chat'),
    path('verify-email/', views.verify_email, name='verify_email'),
    
    # Plantillas
    path('plantillas/', include('pagina.plantillas.urls', namespace='plantillas')),
]
