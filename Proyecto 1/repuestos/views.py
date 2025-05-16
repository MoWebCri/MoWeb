from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Categoria, Repuesto, Carrito
from decimal import Decimal

def home(request):
    categorias = Categoria.objects.all()
    repuestos_destacados = Repuesto.objects.all()[:6]
    return render(request, 'repuestos/home.html', {
        'categorias': categorias,
        'repuestos_destacados': repuestos_destacados
    })

def catalogo(request):
    categorias = Categoria.objects.all()
    categoria_id = request.GET.get('categoria')
    
    if categoria_id:
        repuestos = Repuesto.objects.filter(categoria_id=categoria_id)
    else:
        repuestos = Repuesto.objects.all()
    
    return render(request, 'repuestos/catalogo.html', {
        'categorias': categorias,
        'repuestos': repuestos,
        'categoria_actual': categoria_id
    })

def detalle_repuesto(request, repuesto_id):
    repuesto = get_object_or_404(Repuesto, id=repuesto_id)
    return render(request, 'repuestos/detalle_repuesto.html', {
        'repuesto': repuesto
    })

@login_required
def agregar_al_carrito(request, repuesto_id):
    repuesto = get_object_or_404(Repuesto, id=repuesto_id)
    cantidad = 1  # Siempre agregar solo 1
    
    carrito, created = Carrito.objects.get_or_create(
        usuario=request.user,
        repuesto=repuesto,
        defaults={'cantidad': cantidad}
    )
    
    if not created:
        carrito.cantidad += 1  # Si ya existe, suma 1
        carrito.save()
    
    messages.success(request, 'Repuesto agregado al carrito.')
    return redirect('repuestos:carrito')

@login_required
def carrito(request):
    items = Carrito.objects.filter(usuario=request.user)
    subtotal = sum(item.repuesto.precio * item.cantidad for item in items)
    iva = subtotal * Decimal('0.19')
    total = subtotal + iva
    
    return render(request, 'repuestos/carrito.html', {
        'items': items,
        'subtotal': subtotal,
        'iva': iva,
        'total': total
    })

@login_required
@require_POST
def actualizar_cantidad(request, item_id):
    try:
        item = get_object_or_404(Carrito, id=item_id, usuario=request.user)
        cantidad = int(request.POST.get('cantidad', 1))
        
        if cantidad < 1:
            return JsonResponse({
                'status': 'error',
                'message': 'La cantidad mínima es 1.'
            })
        
        if cantidad > item.repuesto.stock:
            return JsonResponse({
                'status': 'error',
                'message': 'No hay suficiente stock disponible.'
            })
        
        item.cantidad = cantidad
        item.save()
        
        # Calcular nuevos totales
        items = Carrito.objects.filter(usuario=request.user)
        subtotal = sum(item.repuesto.precio * item.cantidad for item in items)
        iva = subtotal * Decimal('0.19')
        total = subtotal + iva
        
        return JsonResponse({
            'status': 'success',
            'cantidad': cantidad,
            'subtotal': float(subtotal),
            'iva': float(iva),
            'total': float(total)
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

@login_required
@require_POST
def eliminar_del_carrito(request, item_id):
    try:
        item = get_object_or_404(Carrito, id=item_id, usuario=request.user)
        item.delete()
        
        # Calcular nuevos totales
        items = Carrito.objects.filter(usuario=request.user)
        subtotal = sum(item.repuesto.precio * item.cantidad for item in items)
        iva = subtotal * Decimal('0.19')
        total = subtotal + iva
        
        return JsonResponse({
            'status': 'success',
            'items_count': items.count(),
            'subtotal': float(subtotal),
            'iva': float(iva),
            'total': float(total)
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })
