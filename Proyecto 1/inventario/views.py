from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Categoria, Producto, Movimiento
from .forms import ProductoForm, CategoriaForm, MovimientoForm

# Create your views here.

@login_required
def lista_productos(request):
    productos = Producto.objects.all().order_by('nombre')
    return render(request, 'inventario/lista_productos.html', {'productos': productos})

@login_required
def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    movimientos = Movimiento.objects.filter(producto=producto).order_by('-fecha')
    return render(request, 'inventario/detalle_producto.html', {
        'producto': producto,
        'movimientos': movimientos
    })

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save()
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('detalle_producto', pk=producto.pk)
    else:
        form = ProductoForm()
    return render(request, 'inventario/crear_producto.html', {'form': form})

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('detalle_producto', pk=producto.pk)
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'inventario/editar_producto.html', {'form': form})

@login_required
def registrar_movimiento(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.producto = producto
            movimiento.usuario = request.user
            
            # Actualizar stock
            if movimiento.tipo == 'entrada':
                producto.stock += movimiento.cantidad
            else:
                if producto.stock >= movimiento.cantidad:
                    producto.stock -= movimiento.cantidad
                else:
                    messages.error(request, 'No hay suficiente stock disponible.')
                    return redirect('registrar_movimiento', pk=pk)
            
            producto.save()
            movimiento.save()
            messages.success(request, 'Movimiento registrado exitosamente.')
            return redirect('detalle_producto', pk=pk)
    else:
        form = MovimientoForm()
    return render(request, 'inventario/registrar_movimiento.html', {
        'form': form,
        'producto': producto
    })

@login_required
def lista_categorias(request):
    categorias = Categoria.objects.all().order_by('nombre')
    return render(request, 'inventario/lista_categorias.html', {'categorias': categorias})

@login_required
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'inventario/crear_categoria.html', {'form': form})
