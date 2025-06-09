# filepath: /home/croy/Documentos/analisisNumerico/final/analisis_numerico/main_numerico/metodo_df_divididas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index),
    path('index/', views.index),
    path('documentacion/', views.documentacion, name='documentacion'),
]