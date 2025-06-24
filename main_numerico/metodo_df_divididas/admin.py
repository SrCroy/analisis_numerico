from django.contrib import admin
from .models import HistorialNewton

@admin.register(HistorialNewton)
class HistorialNewtonAdmin(admin.ModelAdmin):
    list_display = ('usuario_nombre', 'fecha', 'puntos_x', 'puntos_y', 'resultado')
    search_fields = ('usuario_nombre', 'puntos_x', 'puntos_y')
    list_filter = ('fecha',)
