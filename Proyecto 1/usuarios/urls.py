from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'usuarios'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('perfil/', views.perfil, name='perfil'),
    path('notificaciones/', views.notificaciones, name='notificaciones'),
    path('notificaciones/<int:notificacion_id>/marcar-leida/', views.marcar_notificacion_leida, name='marcar_notificacion_leida'),
    path('actividades/', views.actividades, name='actividades'),
    path('2fa/configurar/', views.configurar_2fa, name='configurar_2fa'),
    path('2fa/desactivar/', views.desactivar_2fa, name='desactivar_2fa'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('login/', auth_views.LoginView.as_view(
        template_name='usuarios/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='usuarios/logout.html'
    ), name='logout'),
] 