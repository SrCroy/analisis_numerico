from django.shortcuts import render
from django.db import DataError
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

    derivada_exacta = derivada_forward = derivada_backward = derivada_central = None
    error_forward = error_backward = error_central = None

    if request.method == 'POST':
        form = DifferenceDividedHistoryForm(request.POST)
        if form.is_valid():
            funcion = form.cleaned_data['function']
            x_val   = form.cleaned_data['x_value']
            h       = form.cleaned_data['h_value']

            # --- Parsear y derivar simbólicamente ---
            func = sympify(funcion)
            derivada_exacta_expr = diff(func, x)

            # --- Crear funciones numéricas ---
            f_np  = lambdify(x, func,                'numpy')
            df_np = lambdify(x, derivada_exacta_expr, 'numpy')

            # --- Evaluar numéricamente con lambdify ---
            try:
                f0              = float(f_np(x_val))
                fph             = float(f_np(x_val + h))
                fmh             = float(f_np(x_val - h))
                derivada_exacta = float(df_np(x_val))
            except Exception as e:
                form.add_error('function', f"No pude evaluar la función: {e}")
                return render(request, 'metodo_dn/formulario.html', {
                    'form': form,
                    'user_authenticated': user_authenticated,
                    'historial_actual': historial_actual,
                    'historial_usuario': historial_usuario,
                    'grafica_base64': grafica_base64,
                })

            # --- Cálculo de derivadas numéricas y errores ---
            derivada_forward  = (fph - f0) / h
            derivada_backward = (f0  - fmh) / h
            derivada_central  = (fph - fmh) / (2*h)

            error_forward  = abs((derivada_exacta - derivada_forward)  / derivada_exacta) * 100
            error_backward = abs((derivada_exacta - derivada_backward) / derivada_exacta) * 100
            error_central  = abs((derivada_exacta - derivada_central)  / derivada_exacta) * 100

            if user_authenticated:
                # --- Preparar objeto, sin guardar aún ---
                hobj = form.save(commit=False)
                hobj.user               = request.user
                hobj.derivada_exacta    = derivada_exacta
                hobj.derivada_forward   = derivada_forward
                hobj.derivada_backward  = derivada_backward
                hobj.derivada_central   = derivada_central
                hobj.error_forward      = error_forward
                hobj.error_backward     = error_backward
                hobj.error_central      = error_central

                hobj.formula_forward    = "(f(x+h) - f(x)) / h"
                hobj.formula_backward   = "(f(x) - f(x-h)) / h"
                hobj.formula_central    = "(f(x+h) - f(x-h)) / (2*h)"

                hobj.pasos_forward      = f"({fph} - {f0}) / {h}"
                hobj.pasos_backward     = f"({f0} - {fmh}) / {h}"
                hobj.pasos_central      = f"({fph} - {fmh}) / (2*{h})"

                # --- Intentamos guardar; capturamos DataError si es fuera de rango ---
                try:
                    hobj.save()
                    historial_actual = hobj

                    # --- Historial único ---
                    todos = DifferenceDividedHistory.objects.filter(user=request.user).order_by('-id')
                    unique = {}
                    for e in todos:
                        key = (e.function, e.x_value, e.h_value)
                        if key not in unique:
                            unique[key] = e
                    historial_usuario = list(unique.values())

                    # --- Generar gráfica para autenticados ---
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

                except DataError:
                    # Si el valor es demasiado grande para DecimalField,
                    # omitimos guardar historial y gráfica
                    historial_actual = None

            # --- Renderizamos siempre con datos numéricos ---
            return render(request, 'metodo_dn/formulario.html', {
                'form': form,
                'user_authenticated': user_authenticated,
                'historial_actual': historial_actual,
                'historial_usuario': historial_usuario,
                'grafica_base64': grafica_base64,
                'funcion': funcion,
                'derivada_exacta':    derivada_exacta,
                'derivada_forward':    derivada_forward,
                'error_forward':       error_forward,
                'derivada_backward':   derivada_backward,
                'error_backward':      error_backward,
                'derivada_central':    derivada_central,
                'error_central':       error_central,
            })

    else:
        form = DifferenceDividedHistoryForm()
        if user_authenticated:
            todos = DifferenceDividedHistory.objects.filter(user=request.user).order_by('-id')
            unique = {}
            for e in todos:
                key = (e.function, e.x_value, e.h_value)
                if key not in unique:
                    unique[key] = e
            historial_usuario = list(unique.values())

    # GET o POST inválido: renderizar sin resultados
    return render(request, 'metodo_dn/formulario.html', {
        'form': form,
        'user_authenticated': user_authenticated,
        'historial_actual': historial_actual,
        'historial_usuario': historial_usuario,
        'grafica_base64': grafica_base64,
    })
