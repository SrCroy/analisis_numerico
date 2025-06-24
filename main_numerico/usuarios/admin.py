from django.contrib import admin
from .models import PerfilUsuario

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    # Aquí defines las columnas que quieres ver en la lista
    list_display = (
        'nombre_perfil',  # muestra el nombre completo del User
        'correo',         # muestra el email del User
        'contra',         # muestra el password (hash) del User
        'carrera',
        'carnet',
        'ciclo',
    )
    # Ocultamos la foto en el formulario de edición
    exclude = ('fotografia',)

    # Métodos para tirar de los atributos del User relacionado
    def nombre_perfil(self, obj):
        return obj.user.get_full_name()
    nombre_perfil.short_description = 'Nombre de perfil'
    nombre_perfil.admin_order_field = 'user__first_name'

    def correo(self, obj):
        return obj.user.email
    correo.short_description = 'Correo'
    correo.admin_order_field = 'user__email'

    def contra(self, obj):
        return obj.user.password
    contra.short_description = 'Contraseña'
