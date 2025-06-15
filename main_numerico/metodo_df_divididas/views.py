from django.shortcuts import render, redirect
from .forms import DatosNewtonForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
import io
import base64
from .models import HistorialNewton

# Vistas básicas
def index(request):
    return render(request, 'index.html')

def documentacion(request):
    return render(request, 'documentacion.html')

def menu(request):
    return render(request, 'menu.html')

# Utilidad de formato
def formatear(valor, decimales=4):
    if abs(valor) < 1e-10:
        return f"{0.0:.{decimales}f}"
    return f"{valor:.{decimales}f}"

class DiferenciasDivididasNewton:
    def __init__(self, x, y):
        self.x = np.array(x, dtype=float)
        self.y = np.array(y, dtype=float)
        self.n = len(x)
        self.tabla = np.zeros((self.n, self.n))
        self.pasos = []
        self.__construir_tabla()

    def __construir_tabla(self):
        self.tabla[:, 0] = self.y
        for j in range(1, self.n):
            for i in range(self.n - j):
                self.tabla[i, j] = (self.tabla[i+1, j-1] - self.tabla[i, j-1]) / (self.x[i+j] - self.x[i])
        # Preparar tabla para mostrar
        self.tabla_mostrar = []
        encabezado = ["x", "f(x)"] + [f"D{i}" for i in range(1, self.n)]
        self.tabla_mostrar.append(encabezado)
        for i in range(self.n):
            fila = [formatear(self.x[i]), formatear(self.y[i])]
            for j in range(1, self.n - i):
                fila.append(formatear(self.tabla[i, j]))
            self.tabla_mostrar.append(fila)

    def construir_polinomio_con_pasos(self):
        self.pasos = []
        x = sp.Symbol('x')
        pol = self.tabla[0, 0]
        producto = 1
        self.pasos.append(f"Término 0: {formatear(self.tabla[0, 0])}")
        pol_texto = f"P(x) = {formatear(self.tabla[0, 0])}"

        for i in range(1, self.n):
            coef = self.tabla[0, i]
            factores_lista = [f"(x - {formatear(self.x[j])})" for j in range(i)]
            factores = " * ".join(factores_lista)
            termino_texto = f"{formatear(coef)} * {factores}"
            pol_texto += " + " + termino_texto
            self.pasos.append(f"Término {i}: + {formatear(coef)} * {factores}")
            producto *= (x - self.x[i - 1])
            pol += coef * producto

        pol_expandido = sp.expand(pol)
        self.pasos.append("Polinomio final (expresado): " + pol_texto)
        self.pasos.append("Polinomio expandido: " + str(pol_expandido))
        return pol_expandido, self.pasos, self.tabla_mostrar, pol_texto

def graficar_polinomio(polinomio):
    x = sp.Symbol('x')
    f_lambdified = sp.lambdify(x, polinomio, modules=['numpy'])
    x_vals = np.linspace(-10, 10, 400)
    y_vals = f_lambdified(x_vals)

    plt.figure(figsize=(8, 4))
    plt.plot(x_vals, y_vals, label='Polinomio interpolador', color='blue')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True)
    plt.legend()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    return img_base64

def evaluar_polinomio(polinomio, valor):
    x = sp.Symbol('x')
    return polinomio.evalf(subs={x: valor})

def metodo_newton(request):
    polinomio = None
    resultado = None
    pasos = None
    tabla = None
    grafica_base64 = None
    pol_texto = None
    valor_evaluar = None
    historial = None

    if request.method == 'POST':
        form = DatosNewtonForm(request.POST)
        if form.is_valid():
            try:
                x_valores = [float(i.strip()) for i in form.cleaned_data['x_valores'].split(',')]
                y_valores = [float(i.strip()) for i in form.cleaned_data['y_valores'].split(',')]
            except Exception as e:
                messages.error(request, f"Error en los valores: {str(e)}")
                return render(request, 'metodo_df_divididas/metodo_newton.html', {'form': form})

            valor_evaluar = form.cleaned_data.get('valor_evaluar')
            
            # Procesamiento del método
            metodo = DiferenciasDivididasNewton(x_valores, y_valores)
            polinomio, pasos, tabla, pol_texto = metodo.construir_polinomio_con_pasos()
            
            # Simplificar el polinomio a su mínima expresión
            polinomio_simplificado = sp.simplify(polinomio)
            pol_texto = f"P(x) = {sp.latex(polinomio_simplificado)}"
            
            # Evaluación si existe valor
            if valor_evaluar:
                try:
                    valor_evaluar = float(valor_evaluar)
                    resultado = evaluar_polinomio(polinomio_simplificado, valor_evaluar)
                except ValueError:
                    messages.warning(request, "Valor a evaluar no es numérico")

            # Generar gráfica (solo para usuarios logueados)
            if request.user.is_authenticated:
                grafica_base64 = graficar_polinomio(polinomio_simplificado)

            # Guardar historial SOLO para usuarios autenticados
            if request.user.is_authenticated:
                hist = HistorialNewton(
                    usuario_id=request.user.id,
                    usuario_nombre=f"{request.user.first_name or ''} {request.user.last_name or ''}".strip(),
                    puntos_x=", ".join(map(str, x_valores)),
                    puntos_y=", ".join(map(str, y_valores)),
                    polinomio=pol_texto,
                    pasos="\n".join(pasos) if pasos else ""
                )
                
                if valor_evaluar is not None:
                    hist.valor_evaluado = float(valor_evaluar)
                if resultado is not None:
                    hist.resultado = float(resultado)
                
                hist.save()

    else:
        form = DatosNewtonForm()

    # Obtener historial solo para usuarios logueados
    if request.user.is_authenticated:
        historial = HistorialNewton.objects.filter(usuario_id=request.user.id).order_by('-fecha')[:10]

    # Preparar contexto
    context = {
        'form': form,
        'pol_texto': pol_texto,
        'valor_evaluar': valor_evaluar,
        'resultado': resultado,
        'user': request.user
    }

    # Añadir detalles extras solo para autenticados
    if request.user.is_authenticated:
        context.update({
            'polinomio': polinomio,
            'pasos': pasos,
            'tabla': tabla,
            'grafica_base64': grafica_base64,
            'historial': historial
        })

    return render(request, 'metodo_df_divididas/metodo_newton.html', context)