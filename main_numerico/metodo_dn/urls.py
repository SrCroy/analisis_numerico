# main_numerico/metodo_dn/urls.py

from django.urls import path
from .views import diferenciacion_view

app_name = 'metodo_dn'

urlpatterns = [
    # Ruta única para tu método de diferenciación numérica
    path('diferenciacion/', diferenciacion_view, name='diferenciacion_form'),
]
