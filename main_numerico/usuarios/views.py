from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UsuarioForm, LoginForm
from .models import Usuario
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import DifferenceDividedHistory
from .forms import DiferenciacionForm
from sympy import symbols, sympify, diff, lambdify
import matplotlib.pyplot as plt
import io
import base64
import urllib.parse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from sympy import symbols, diff, lambdify, sympify
import matplotlib.pyplot as plt
import io
import base64
import urllib


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
###########################################################################################################################################################

def diferencias(request):
    resultado = {}
    
    if request.method == 'POST':
        # Obtener datos del formulario
        funcion = request.POST.get('function')
        x_value = request.POST.get('x-value')
        h_value = request.POST.get('h-value')
        
        try:
            # Convertir valores a float
            valor_x = float(x_value)
            valor_h = float(h_value)
            
            # Procesar la función
            x = symbols('x')
            ecuacion = sympify(funcion)
            f = lambdify(x, ecuacion)
            
            # Calcular derivada exacta
            derivada_exacta = diff(ecuacion, x)
            derivada_exacta_func = lambdify(x, derivada_exacta)
            derivada_exacta_val = round(derivada_exacta_func(valor_x), 4)
            
            # Función para calcular derivada forward
            def derivada_forward(f, x, h):
                f_x = round(f(x), 4)
                f_x_plus_h = round(f(x + h), 4)
                resultado = round((f_x_plus_h - f_x) / h, 4)
                formula_sustituida = f"({f_x_plus_h} - {f_x}) / {h}"
                pasos = [
                    f"f(x) = {f_x}",
                    f"f(x + h) = {f_x_plus_h}",
                    f"({f_x_plus_h} - {f_x}) / {h} = {resultado}"
                ]
                return resultado, formula_sustituida, pasos
            
            # Función para calcular derivada backward
            def derivada_backward(f, x, h):
                f_x = round(f(x), 4)
                f_x_minus_h = round(f(x - h), 4)
                resultado = round((f_x - f_x_minus_h) / h, 4)
                formula_sustituida = f"({f_x} - {f_x_minus_h}) / {h}"
                pasos = [
                    f"f(x) = {f_x}",
                    f"f(x - h) = {f_x_minus_h}",
                    f"({f_x} - {f_x_minus_h}) / {h} = {resultado}"
                ]
                return resultado, formula_sustituida, pasos
            
            # Función para calcular derivada central
            def derivada_central(f, x, h):
                f_x = round(f(x), 4)
                f_x_plus_h = round(f(x + h), 4)
                f_x_minus_h = round(f(x - h), 4)
                resultado = round((f_x_plus_h - f_x_minus_h) / (2 * h), 4)
                formula_sustituida = f"({f_x_plus_h} - {f_x_minus_h}) / (2 * {h})"
                pasos = [
                    f"f(x) = {f_x}",
                    f"f(x + h) = {f_x_plus_h}",
                    f"f(x - h) = {f_x_minus_h}",
                    f"({f_x_plus_h} - {f_x_minus_h}) / (2 * {h}) = {resultado}"
                ]
                return resultado, formula_sustituida, pasos
            
            # Calcular derivadas numéricas
            derivada_fwd, formula_fwd, pasos_fwd = derivada_forward(f, valor_x, valor_h)
            derivada_bwd, formula_bwd, pasos_bwd = derivada_backward(f, valor_x, valor_h)
            derivada_cen, formula_cen, pasos_cen = derivada_central(f, valor_x, valor_h)
            
            # Calcular errores
            def calcular_errores(derivada_fwd, derivada_bwd, derivada_cen, derivada_exacta_val):
                error_fwd = abs(derivada_fwd - derivada_exacta_val)
                error_bwd = abs(derivada_bwd - derivada_exacta_val)
                error_cen = abs(derivada_cen - derivada_exacta_val)
                return {
                    'error_fwd': round(error_fwd, 4),
                    'error_bwd': round(error_bwd, 4),
                    'error_cen': round(error_cen, 4)
                }
            
            errores = calcular_errores(derivada_fwd, derivada_bwd, derivada_cen, derivada_exacta_val)
            
            # Guardar en historial si el usuario está autenticado
            if request.user.is_authenticated:
                DifferenceDividedHistory.objects.create(
                    user=request.user,
                    function=funcion,
                    x_value=valor_x,
                    h_value=valor_h,
                    derivada_fwd=derivada_fwd,
                    derivada_bwd=derivada_bwd,
                    derivada_cen=derivada_cen,
                    derivada_exacta=derivada_exacta_val,
                    error_fwd=errores['error_fwd'],
                    error_bwd=errores['error_bwd'],
                    error_cen=errores['error_cen']
                )
            
            # Generar gráfica
            x_vals = [valor_x - 2*valor_h, valor_x - valor_h, valor_x, valor_x + valor_h, valor_x + 2*valor_h]
            y_vals = [f(val) for val in x_vals]
            
            plt.figure()
            plt.plot(x_vals, y_vals, 'b-', label='Función')
            plt.plot(valor_x, f(valor_x), 'ro', label='Punto de Evaluación')
            plt.xlabel('x')
            plt.ylabel('f(x)')
            plt.title('Gráfica de la Función')
            plt.legend()
            plt.grid(True)
            
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            grafica_url = 'data:image/png;base64,' + urllib.parse.quote(string)
            plt.close()
            
            # Preparar resultados para el template
            resultado = {
                'funcion': funcion,
                'x_value': valor_x,
                'h_value': valor_h,
                'forward': {
                    'resultado': derivada_fwd,
                    'formula': formula_fwd,
                    'pasos': pasos_fwd,
                    'error': errores['error_fwd']
                },
                'backward': {
                    'resultado': derivada_bwd,
                    'formula': formula_bwd,
                    'pasos': pasos_bwd,
                    'error': errores['error_bwd']
                },
                'central': {
                    'resultado': derivada_cen,
                    'formula': formula_cen,
                    'pasos': pasos_cen,
                    'error': errores['error_cen']
                },
                'exacta': {
                    'formula': str(derivada_exacta),
                    'resultado': derivada_exacta_val
                },
                'grafica': grafica_url
            }
            
            messages.success(request, 'Cálculo de derivadas completado correctamente.')
            
        except ValueError as e:
            messages.error(request, f'Error en los valores ingresados: {str(e)}')
        except SyntaxError as e:
            messages.error(request, f'Error en la sintaxis de la función: {str(e)}')
        except Exception as e:
            messages.error(request, f'Error durante el cálculo: {str(e)}')
    
    return render(request, 'diferencias.html', {
        'resultado': resultado,
        'messages': messages.get_messages(request)
    })