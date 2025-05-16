from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Curso, Carrito, ItemCarrito, Compra, DetalleCompra

# Create your views here.

def lista_cursos(request):
    cursos = Curso.objects.filter(activo=True)
    return render(request, 'cursos/lista_cursos.html', {
        'cursos': cursos,
        'titulo': 'Catálogo de Cursos'
    })

def detalle_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id, activo=True)
    en_carrito = False
    comprado = False
    
    if request.user.is_authenticated:
        en_carrito = curso.esta_en_carrito(request.user)
        comprado = curso.esta_comprado(request.user)
    
    return render(request, 'cursos/detalle_curso.html', {
        'curso': curso,
        'titulo': curso.titulo,
        'en_carrito': en_carrito,
        'comprado': comprado
    })

@login_required
def agregar_al_carrito(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id, activo=True)
    
    # Verificar si el curso ya está en el carrito
    if curso.esta_en_carrito(request.user):
        messages.warning(request, 'Este curso ya está en tu carrito.')
        return redirect('cursos:detalle_curso', curso_id=curso.id)
    
    # Verificar si el curso ya fue comprado
    if curso.esta_comprado(request.user):
        messages.warning(request, 'Ya has comprado este curso.')
        return redirect('cursos:detalle_curso', curso_id=curso.id)
    
    # Obtener o crear el carrito del usuario
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    
    # Agregar el curso al carrito
    ItemCarrito.objects.create(carrito=carrito, curso=curso)
    
    messages.success(request, f'¡{curso.titulo} agregado al carrito exitosamente!')
    return redirect('cursos:detalle_curso', curso_id=curso.id)

@login_required
def ver_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    return render(request, 'cursos/carrito.html', {
        'carrito': carrito,
        'titulo': 'Mi Carrito'
    })

@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    curso_titulo = item.curso.titulo
    item.delete()
    messages.success(request, f'¡{curso_titulo} eliminado del carrito!')
    return redirect('cursos:ver_carrito')

@login_required
@transaction.atomic
def realizar_compra(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    
    if not carrito.items.exists():
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('cursos:ver_carrito')
    
    # Crear la compra
    compra = Compra.objects.create(
        usuario=request.user,
        total=carrito.total,
        estado='completada'
    )
    
    # Crear los detalles de la compra
    for item in carrito.items.all():
        DetalleCompra.objects.create(
            compra=compra,
            curso=item.curso,
            precio=item.curso.precio
        )
    
    # Vaciar el carrito
    carrito.items.all().delete()
    
    messages.success(request, '¡Compra realizada con éxito! Ya puedes acceder a tus cursos.')
    return redirect('cursos:mis_cursos')

@login_required
def mis_cursos(request):
    compras = Compra.objects.filter(
        usuario=request.user,
        estado='completada'
    ).prefetch_related('cursos')
    
    return render(request, 'cursos/mis_cursos.html', {
        'compras': compras,
        'titulo': 'Mis Cursos'
    })
