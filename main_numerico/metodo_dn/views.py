# main_numerico/metodo_dn/views.py

from django.shortcuts import render
from .forms import DifferenceDividedHistoryForm
from .models import DifferenceDividedHistory
from sympy import sympify, symbols, diff, lambdify
import matplotlib.pyplot as plt
import numpy as np
import io, base64

x = symbols('x')

def diferenciacion_view(request):
    user_authenticated = request.user.is_authenticated
    historial_usuario = None
    historial_actual = None
    grafica_base64 = None
    funcion = None

    if request.method == 'POST':
        form = DifferenceDividedHistoryForm(request.POST)
        if form.is_valid():
            funcion = form.cleaned_data['function']
            x_val = form.cleaned_data['x_value']
            h = form.cleaned_data['h_value']
            try:
                # --- Cálculo simbólico ---
                func = sympify(funcion)
                derivada_exacta_expr = diff(func, x)
                derivada_exacta = float(derivada_exacta_expr.evalf(subs={x: x_val}))

                # --- Evaluaciones numéricas ---
                f0 = float(func.evalf(subs={x: x_val}))
                fph = float(func.evalf(subs={x: x_val + h}))
                fmh = float(func.evalf(subs={x: x_val - h}))

                fwd = (fph - f0) / h
                bwd = (f0 - fmh) / h
                cen = (fph - fmh) / (2*h)

                error_fwd = abs((derivada_exacta - fwd) / derivada_exacta) * 100
                error_bwd = abs((derivada_exacta - bwd) / derivada_exacta) * 100
                error_cen = abs((derivada_exacta - cen) / derivada_exacta) * 100

                if user_authenticated:
                    # --- Guardar historial ---
                    hobj = form.save(commit=False)
                    hobj.user = request.user
                    hobj.derivada_exacta = derivada_exacta
                    hobj.derivada_forward = fwd
                    hobj.derivada_backward = bwd
                    hobj.derivada_central = cen
                    hobj.error_forward = error_fwd
                    hobj.error_backward = error_bwd
                    hobj.error_central = error_cen

                    hobj.formula_forward = "(f(x+h) - f(x)) / h"
                    hobj.formula_backward = "(f(x) - f(x-h)) / h"
                    hobj.formula_central = "(f(x+h) - f(x-h)) / (2*h)"

                    hobj.pasos_forward = f"({fph} - {f0}) / {h}"
                    hobj.pasos_backward = f"({f0} - {fmh}) / {h}"
                    hobj.pasos_central = f"({fph} - {fmh}) / (2*{h})"

                    hobj.save()
                    historial_actual = hobj

                    # --- Historial único para tabla ---
                    todos = DifferenceDividedHistory.objects.filter(user=request.user).order_by('-id')
                    unique = {}
                    for e in todos:
                        key = (e.function, e.x_value, e.h_value)
                        if key not in unique:
                            unique[key] = e
                    historial_usuario = list(unique.values())

                    # --- Generar gráfica ---
                    f_np = lambdify(x, func, 'numpy')
                    df_np = lambdify(x, derivada_exacta_expr, 'numpy')
                    xs = np.linspace(x_val - 3*h, x_val + 3*h, 200)
                    ys = f_np(xs)
                    dys = df_np(xs)
                    fig, ax = plt.subplots()
                    ax.plot(xs, ys, label='f(x)')
                    ax.plot(xs, dys, label="f'(x)")
                    ax.axvline(x=x_val, linestyle='--', label=f"x={x_val}")
                    ax.legend()
                    buf = io.BytesIO()
                    plt.savefig(buf, format='png', bbox_inches='tight')
                    plt.close(fig)
                    grafica_base64 = base64.b64encode(buf.getvalue()).decode()

                # al final del POST renderizamos
                return render(request, 'metodo_dn/formulario.html', {
                    'form': form,
                    'user_authenticated': user_authenticated,
                    'historial_actual': historial_actual,
                    'funcion': funcion,
                    'historial_usuario': historial_usuario,
                    'grafica_base64': grafica_base64,
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
        # GET: solo preparar formulario y, si hay usuario, historial_usuario
        form = DifferenceDividedHistoryForm()
        if user_authenticated:
            todos = DifferenceDividedHistory.objects.filter(user=request.user).order_by('-id')
            unique = {}
            for e in todos:
                key = (e.function, e.x_value, e.h_value)
                if key not in unique:
                    unique[key] = e
            historial_usuario = list(unique.values())

    # render final para GET o POST inválido
    return render(request, 'metodo_dn/formulario.html', {
        'form': form,
        'user_authenticated': user_authenticated,
        'historial_actual': historial_actual,
        'funcion': funcion,
        'historial_usuario': historial_usuario,
        'grafica_base64': grafica_base64,
        # datos numéricos para anónimos
        'derivada_exacta': locals().get('derivada_exacta'),
        'derivada_forward': locals().get('fwd'),
        'derivada_backward': locals().get('bwd'),
        'derivada_central': locals().get('cen'),
        'error_forward': locals().get('error_fwd'),
        'error_backward': locals().get('error_bwd'),
        'error_central': locals().get('error_cen'),
    })
