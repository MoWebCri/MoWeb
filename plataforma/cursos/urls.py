from django.urls import path
from . import views

app_name = 'cursos'

urlpatterns = [
    path('', views.lista_cursos, name='lista_cursos'),
    path('curso/<int:curso_id>/', views.detalle_curso, name='detalle_curso'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:curso_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/comprar/', views.realizar_compra, name='realizar_compra'),
    path('mis-cursos/', views.mis_cursos, name='mis_cursos'),
] 