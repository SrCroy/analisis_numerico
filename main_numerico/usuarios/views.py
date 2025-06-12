from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UsuarioForm, LoginForm
from .models import Usuario

def registro_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Usuario creado exitosamente!')
            return redirect('login')  # Redirigir al login tras registro
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/crear_usuario.html', {'form': form})

def login_usuario(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            contrasena = form.cleaned_data['contrasena']
            try:
                usuario = Usuario.objects.get(correo=correo)
                if usuario.contrasena == contrasena:
                    # Guardar usuario en sesión
                    request.session['usuario_id'] = usuario.id
                    request.session['usuario_nombre'] = usuario.nombre
                    messages.success(request, f'Bienvenido {usuario.nombre}')
                    return redirect('index')  # Página principal tras login
                else:
                    messages.error(request, 'Contraseña incorrecta')
            except Usuario.DoesNotExist:
                messages.error(request, 'Correo no registrado')
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})

def logout_usuario(request):
    try:
        del request.session['usuario_id']
        del request.session['usuario_nombre']
    except KeyError:
        pass
    messages.info(request, 'Has cerrado sesión')
    return redirect('login')
