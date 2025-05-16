from django.urls import path
from .views import contacto_view

app_name = 'contacto'

urlpatterns = [
    path('', contacto_view, name='contacto'),
] 