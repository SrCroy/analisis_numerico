from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UsuarioForm

def registro_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Usuario creado exitosamente!')
            return redirect('index')  # o cualquier ruta válida
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/crear_usuario.html', {'form': form})
