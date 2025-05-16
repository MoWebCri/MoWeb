from django.urls import path
from . import views

app_name = 'repuestos'

urlpatterns = [
    path('', views.home, name='home'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('repuesto/<int:repuesto_id>/', views.detalle_repuesto, name='detalle_repuesto'),
    path('carrito/', views.carrito, name='carrito'),
    path('agregar-al-carrito/<int:repuesto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('actualizar-cantidad/<int:item_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('eliminar-del-carrito/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
] 