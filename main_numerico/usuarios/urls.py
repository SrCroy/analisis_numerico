# usuarios/urls.py

from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Registro de nuevo usuario
    path('registro/', views.registro_usuario, name='registro'),

    # Login de usuario
    path('login/', views.login_usuario, name='login'),

    # Logout de usuario
    path('logout/', views.logout_usuario, name='logout'),

    # Ver perfil
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),

    # Editar perfil
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
]
