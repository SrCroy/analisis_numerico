# usuarios/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect

from .forms import RegistroUsuarioForm, LoginForm, EditarPerfilForm
from .models import PerfilUsuario
from metodo_df_divididas.models import HistorialNewton
from metodo_dn.models import DifferenceDividedHistory

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            PerfilUsuario.objects.create(
                user=user,
                carrera=form.cleaned_data['carrera'],
                carnet=form.cleaned_data['carnet'],
                ciclo=form.cleaned_data['ciclo'],
                fotografia=form.cleaned_data.get('fotografia')
            )
            user = authenticate(username=user.username, password=form.cleaned_data['password'])
            if user:
                login(request, user)
                messages.success(request, f'¡Bienvenido {user.first_name}! Registro exitoso.')
                return redirect('index')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'usuarios/crear_usuario.html', {'form': form})

@csrf_protect
def login_usuario(request):
    if request.user.is_authenticated:
        messages.info(request, 'Ya has iniciado sesión')
        return redirect('index')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            contrasena = form.cleaned_data['contrasena']
            try:
                user_obj = User.objects.get(email=correo)
                username = user_obj.username
            except User.DoesNotExist:
                username = None

            user = authenticate(request, username=username, password=contrasena) if username else None

            if user:
                login(request, user)
                messages.success(request, f'Bienvenido {user.first_name or user.username}')
                next_url = request.GET.get('next', 'index')
                return redirect(next_url)
            else:
                messages.error(request, 'Correo o contraseña incorrectos')
                return redirect('usuarios:login')
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
    return redirect('usuarios:login')

@login_required
def perfil_usuario(request):
    try:
        perfil = PerfilUsuario.objects.get(user=request.user)
    except PerfilUsuario.DoesNotExist:
        perfil = None
        messages.info(request, "Aún no tienes un perfil. Por favor complétalo.")

    historial_newton = []
    historial_dn = []
    if perfil:
        historial_newton = HistorialNewton.objects.filter(usuario_id=request.user.id).order_by('-fecha')
        historial_dn = DifferenceDividedHistory.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'usuarios/perfil.html', {
        'perfil': perfil,
        'historial_newton': historial_newton,
        'historial_dn': historial_dn,
    })

@login_required
def editar_perfil(request):
    try:
        perfil = PerfilUsuario.objects.get(user=request.user)
    except PerfilUsuario.DoesNotExist:
        messages.error(request, "No se encontró tu perfil para editar.")
        return redirect('usuarios:perfil_usuario')

    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.user.first_name = form.cleaned_data['first_name']
            perfil.user.last_name = form.cleaned_data['last_name']
            password = form.cleaned_data.get('password')
            if password:
                perfil.user.set_password(password)
                perfil.user.save()
                update_session_auth_hash(request, perfil.user)
            else:
                perfil.user.save()
            perfil.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('index')
    else:
        form = EditarPerfilForm(instance=perfil, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        })

    return render(request, 'usuarios/editar_perfil.html', {
        'form': form,
        'perfil': perfil
    })
