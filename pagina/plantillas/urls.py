from django.urls import path
from pagina import views

app_name = 'plantillas'

urlpatterns = [
    path('negocio/', views.plantilla_negocio, name='plantilla_negocio'),
    path('portafolio/', views.plantilla_portafolio, name='plantilla_portafolio'),
    path('elearning/', views.plantilla_elearning, name='plantilla_elearning'),
    path('repuestos/', views.plantilla_repuestos, name='plantilla_repuestos'),
] 