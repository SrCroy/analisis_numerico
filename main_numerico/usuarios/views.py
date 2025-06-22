from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import RegistroUsuarioForm, LoginForm
from .models import PerfilUsuario
from django.contrib.auth.models import User

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            # Crear usuario
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Crear perfil
            PerfilUsuario.objects.create(
                user=user,
                carrera=form.cleaned_data['carrera'],
                carnet=form.cleaned_data['carnet'],
                ciclo=form.cleaned_data['ciclo'],
                fotografia=form.cleaned_data.get('fotografia')
            )

            # Autenticar y loguear
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {first_name}! Registro exitoso.')
                return redirect('index')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'usuarios/crear_usuario.html', {'form': form})

def login_usuario(request):
    if request.user.is_authenticated:
        messages.info(request, 'Ya has iniciado sesión')
        return redirect('index')
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            contrasena = form.cleaned_data['contrasena']

            # Buscar usuario por correo
            try:
                user_obj = User.objects.get(email=correo)
                username = user_obj.username
            except User.DoesNotExist:
                username = None

            if username:
                user = authenticate(request, username=username, password=contrasena)
            else:
                user = None
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido {user.first_name or user.username}')
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