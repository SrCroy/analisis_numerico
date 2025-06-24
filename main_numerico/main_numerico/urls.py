# main_numerico/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Vistas de diferencias divididas
from metodo_df_divididas.views import (
    index as df_index,
    documentacion as df_documentacion,
    menu as df_menu,
    metodo_newton as df_metodo_newton,
)

# Vistas de perfil/edición expuestas en raíz
from usuarios.views import perfil_usuario, editar_perfil

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas de la app de diferencias divididas
    path('', df_index, name='index'),
    path('documentacion/', df_documentacion, name='documentacion'),
    path('menu/', df_menu, name='menu'),
    path('newton/', df_metodo_newton, name='metodo_newton'),

    # Perfil y edición en la raíz
    path('perfil/', perfil_usuario, name='perfil_usuario'),
    path('perfil/editar/', editar_perfil, name='editar_perfil'),

    # Tu app de usuarios bajo /usuarios/
    path('usuarios/', include('usuarios.urls', namespace='usuarios')),

    # App de diferenciación numérica
    path('diferenciacion/', include('metodo_dn.urls', namespace='metodo_dn')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
