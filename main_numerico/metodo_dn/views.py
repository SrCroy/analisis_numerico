from django.shortcuts import render, redirect
from .forms import DifferenceDividedHistoryForm
from .models import DifferenceDividedHistory
from sympy import sympify, symbols, diff, lambdify
import matplotlib.pyplot as plt
import numpy as np
import io, base64
from django.contrib.auth.decorators import login_required


x = symbols('x')


# Vistas básicas
def index(request):
    return render(request, 'index.html')

def documentacion(request):
    return render(request, 'documentacion.html')

def menu(request):
    return render(request, 'menu.html')

def diferenciacion_view(request):
    historial_usuario = None
    user_authenticated = request.user.is_authenticated
    historial_actual = None
    grafica_base64 = None

    if request.method == 'POST':
        form = DifferenceDividedHistoryForm(request.POST)
        if form.is_valid():
            function_str = form.cleaned_data['function']
            x_val = form.cleaned_data['x_value']
            h = form.cleaned_data['h_value']

            try:
                func = sympify(function_str)
                derivada_exacta_expr = diff(func, x)
                derivada_exacta = float(derivada_exacta_expr.evalf(subs={x: x_val}))
                f_x = float(func.evalf(subs={x: x_val}))
                f_x_plus_h = float(func.evalf(subs={x: x_val + h}))
                f_x_minus_h = float(func.evalf(subs={x: x_val - h}))

                fwd = (f_x_plus_h - f_x) / h
                bwd = (f_x - f_x_minus_h) / h
                cen = (f_x_plus_h - f_x_minus_h) / (2 * h)

                error_fwd = abs((derivada_exacta - fwd) / derivada_exacta) * 100
                error_bwd = abs((derivada_exacta - bwd) / derivada_exacta) * 100
                error_cen = abs((derivada_exacta - cen) / derivada_exacta) * 100

                if user_authenticated:
                    historial = form.save(commit=False)
                    historial.user = request.user
                    historial.derivada_forward = fwd
                    historial.derivada_backward = bwd
                    historial.derivada_central = cen
                    historial.derivada_exacta = derivada_exacta
                    historial.error_forward = error_fwd
                    historial.error_backward = error_bwd
                    historial.error_central = error_cen
                    historial.formula_forward = "f(x+h) - f(x) / h"
                    historial.formula_backward = "f(x) - f(x-h) / h"
                    historial.formula_central = "f(x+h) - f(x-h) / (2*h)"
                    historial.pasos_forward = f"({f_x_plus_h} - {f_x}) / {h}"
                    historial.pasos_backward = f"({f_x} - {f_x_minus_h}) / {h}"
                    historial.pasos_central = f"({f_x_plus_h} - {f_x_minus_h}) / (2*{h})"
                    historial.save()
                    historial_actual = historial  # cálculo actual para mostrar

                    # Obtener historial único por ejercicio
                    all_historial = DifferenceDividedHistory.objects.filter(user=request.user).order_by('-id')
                    ejercicios_unicos = {}
                    for h_obj in all_historial:
                        key = (h_obj.function, h_obj.x_value, h_obj.h_value)
                        if key not in ejercicios_unicos:
                            ejercicios_unicos[key] = h_obj
                    historial_usuario = list(ejercicios_unicos.values())

                    # Generar gráfica
                    f_np = lambdify(x, func, modules=['numpy'])
                    df_np = lambdify(x, derivada_exacta_expr, modules=['numpy'])

                    x_vals = np.linspace(x_val - 3*h, x_val + 3*h, 100)
                    y_vals = f_np(x_vals)
                    dy_vals = df_np(x_vals)

                    fig, ax = plt.subplots()
                    ax.plot(x_vals, y_vals, label='f(x)', color='blue')
                    ax.plot(x_vals, dy_vals, label="f'(x)", color='green')
                    ax.axvline(x=x_val, color='red', linestyle='--', label=f"x = {x_val}")
                    ax.legend()
                    ax.set_title('Función y Derivada Exacta')
                    ax.grid(True)

                    buf = io.BytesIO()
                    plt.savefig(buf, format='png', bbox_inches='tight')
                    plt.close(fig)
                    grafica_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

                else:
                    # Usuario anónimo: no guarda ni historial, ni gráfica, solo resultados básicos
                    historial_actual = None
                    historial_usuario = None

                # Renderizar resultado directo en el formulario
                return render(request, 'metodo_dn/formulario.html', {
                    'form': form,
                    'user_authenticated': user_authenticated,
                    'historial_usuario': historial_usuario,
                    'historial_actual': historial_actual,
                    'grafica_base64': grafica_base64,
                    # Variables para mostrar resultados básicos a anónimos
                    'derivada_exacta': derivada_exacta,
                    'derivada_forward': fwd,
                    'derivada_backward': bwd,
                    'derivada_central': cen,
                    'error_forward': error_fwd,
                    'error_backward': error_bwd,
                    'error_central': error_cen,
                })

            except Exception as e:
                form.add_error('function', f"Error en la función: {e}")
    else:
        form = DifferenceDividedHistoryForm()

        if user_authenticated:
            all_historial = DifferenceDividedHistory.objects.filter(user=request.user).order_by('-id')
            ejercicios_unicos = {}
            for h_obj in all_historial:
                key = (h_obj.function, h_obj.x_value, h_obj.h_value)
                if key not in ejercicios_unicos:
                    ejercicios_unicos[key] = h_obj
            historial_usuario = list(ejercicios_unicos.values())
        else:
            historial_usuario = None

        historial_actual = None
        grafica_base64 = None

    return render(request, 'metodo_dn/formulario.html', {
        'form': form,
        'user_authenticated': user_authenticated,
        'historial_usuario': historial_usuario,
        'historial_actual': historial_actual,
        'grafica_base64': grafica_base64,
    })
