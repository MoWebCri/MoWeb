from django.contrib import admin
from django.urls import path, include
from pagina.views import inicio

# Ruta raíz (inicial) para redirigir a la vista de inicio
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('pagina.urls')),  # Movemos las URLs de pagina a la raíz
]
    