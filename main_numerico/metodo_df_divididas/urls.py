# filepath: main_numerico/metodo_df_divididas/urls.py

from django.urls import path
from .views import index, documentacion, menu, metodo_newton

app_name = 'metodo_df_divididas'

urlpatterns = [
    # GET /divididas/                → vista index()
    path('', index, name='index'),

    # GET /divididas/documentacion/  → vista documentacion()
    path('documentacion/', documentacion, name='documentacion'),

    # GET /divididas/menu/           → vista menu()
    path('menu/', menu, name='menu'),

    # GET/POST /divididas/newton/    → vista metodo_newton()
    path('newton/', metodo_newton, name='metodo_newton'),
]
