function recuperarCalculo(puntos_x, puntos_y, valor_evaluar) {
    document.getElementById('id_x_valores').value = puntos_x.trim();
    document.getElementById('id_y_valores').value = puntos_y.trim();

    if (valor_evaluar && valor_evaluar != 'None') {
        document.getElementById('id_valor_evaluar').value = valor_evaluar;
    } else {
        document.getElementById('id_valor_evaluar').value = '';
    }

    // Mostrar notificación
    const toast = document.createElement('div');
    toast.className = 'position-fixed bottom-0 end-0 p-3';
    toast.innerHTML = `
                <div class="toast show" role="alert" aria-live="assertive" aria-atomic="true">
                    <div class="toast-header bg-success text-dark">
                        <strong class="me-auto">Datos recuperados</strong>
                        <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                    </div>
                    <div class="toast-body">
                        Los datos del cálculo han sido cargados en el formulario.
                    </div>
                </div>
            `;
    document.body.appendChild(toast);

    // Eliminar después de 3 segundos
    setTimeout(() => toast.remove(), 3000);
}

// Efecto de escritura para inputs
document.querySelectorAll('.terminal-input').forEach(input => {
    input.addEventListener('focus', function () {
        this.style.boxShadow = '0 0 10px rgba(51, 255, 51, 0.8)';
    });

    input.addEventListener('blur', function () {
        this.style.boxShadow = 'none';
    });
});