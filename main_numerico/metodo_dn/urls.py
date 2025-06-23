from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Página principal
    path('documentacion/', views.documentacion, name='documentacion'),  # Documentación del método
    path('menu/', views.menu, name='menu'),  # Menú de métodos
    path('diferenciacion/', views.diferenciacion_view, name='diferenciacion_form'), # Vista del formulario y resultados
]
