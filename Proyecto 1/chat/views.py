from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ChatMensaje
from repuestos.models import Repuesto

@login_required
def chat_view(request):
    mensajes = ChatMensaje.objects.filter(usuario=request.user).order_by('-fecha')[:10]
    return render(request, 'chat/chat.html', {
        'mensajes': mensajes
    })

@login_required
def enviar_mensaje(request):
    if request.method == 'POST':
        try:
            marca = request.POST.get('marca_auto', '').strip()
            modelo = request.POST.get('modelo_auto', '').strip()
            repuesto = request.POST.get('repuesto_buscado', '').strip()
            
            # Buscar repuestos
            repuestos = Repuesto.objects.filter(
                nombre__icontains=repuesto,
                marca__icontains=marca,
                modelo_auto__icontains=modelo
            )[:5]
            
            # Guardar mensaje
            mensaje_texto = f"Buscando {repuesto} para {marca} {modelo}"
            ChatMensaje.objects.create(
                usuario=request.user,
                mensaje=mensaje_texto
            )
            
            # Preparar respuesta
            if repuestos.exists():
                respuesta = []
                for r in repuestos:
                    respuesta.append({
                        'nombre': r.nombre,
                        'marca': r.marca,
                        'modelo': r.modelo_auto,
                        'precio': float(r.precio),
                        'stock': r.stock,
                        'categoria': r.categoria.nombre,
                        'descripcion': r.descripcion
                    })
            else:
                respuesta = [{
                    'error': f"No encontré {repuesto} para {marca} {modelo}",
                    'sugerencias': [
                        "Filtro de aceite",
                        "Pastillas de freno",
                        "Bujías",
                        "Correa de distribución",
                        "Amortiguadores"
                    ]
                }]
            
            return JsonResponse({
                'status': 'success',
                'repuestos': respuesta
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'error': str(e)
            })
    
    return JsonResponse({
        'status': 'error',
        'error': 'Método no permitido'
    }) 