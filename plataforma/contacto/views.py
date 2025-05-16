from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactoForm

# Create your views here.

def contacto_view(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            mensaje = form.save()
            messages.success(
                request, 
                '¡Gracias por contactarnos! Te responderemos a la brevedad.'
            )
            return redirect('contacto')
        else:
            messages.error(
                request, 
                'Por favor corrige los errores en el formulario.'
            )
    else:
        form = ContactoForm()
    
    return render(request, 'contacto/contacto.html', {
        'form': form,
        'titulo': 'Contacto'
    })
