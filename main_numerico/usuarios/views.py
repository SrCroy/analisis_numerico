from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UsuarioForm, LoginForm
from django.contrib.auth.models import User

def registro_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            nombre = form.cleaned_data.get('nombre', '')
            contrasena = form.cleaned_data['contrasena']
            
            # Verificar si el usuario ya existe
            if User.objects.filter(username=correo).exists():
                messages.error(request, 'Este correo ya está registrado')
                return redirect('registro')
            
            # Crear usuario con Django auth
            user = User.objects.create_user(
                username=correo,
                email=correo,
                password=contrasena,
                first_name=nombre
            )
            
            # Autenticar y loguear al usuario directamente después del registro
            user = authenticate(username=correo, password=contrasena)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {nombre}! Registro exitoso.')
                return redirect('index')
            
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/crear_usuario.html', {'form': form})

def login_usuario(request):
    # Si el usuario ya está autenticado, redirigir al index
    if request.user.is_authenticated:
        messages.info(request, 'Ya has iniciado sesión')
        return redirect('index')
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            contrasena = form.cleaned_data['contrasena']
            user = authenticate(request, username=correo, password=contrasena)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido {user.first_name or user.username}')
                
                # Redirigir a 'next' si existe en la URL
                next_url = request.GET.get('next', 'index')
                return redirect(next_url)
            else:
                messages.error(request, 'Correo o contraseña incorrectos')
                return redirect('login')
    else:
        form = LoginForm()
    
    return render(request, 'usuarios/login.html', {
        'form': form,
        'next': request.GET.get('next', '')
    })

def logout_usuario(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'Has cerrado sesión correctamente')
    else:
        messages.warning(request, 'No habías iniciado sesión')
    
    return redirect('login')