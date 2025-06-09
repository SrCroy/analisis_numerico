// Configuración de terminales
const commands = {
    python: {
        win: [
            '<span class="text-success">C:\\Users\\mincho></span> Descargar Python desde python.org/downloads',
            '<span class="text-success">C:\\Users\\mincho></span> Ejecutar instalador y marcar "Add Python to PATH"',
            '<span class="text-success">C:\\Users\\mincho></span> python --version',
            'Python 3.x.x',
            '<span class="text-success">C:\\Users\\mincho></span>'
        ],
        deb: [
            '<span class="text-success">mincho@debian:</span>$ sudo apt update',
            '<span class="text-success">mincho@debian:</span>$ sudo apt install python3 python3-pip',
            'Leyendo lista de paquetes...',
            'Instalando python3 python3-pip...',
            '<span class="text-success">mincho@debian:</span>$ python3 --version',
            'Python 3.x.x',
            '<span class="text-success">mincho@debian:</span>$'
        ]
    },
    numpy: {
        win: [
            '<span class="text-success">C:\\Users\\mincho></span> pip install numpy',
            'Collecting numpy...',
            'Successfully installed numpy',
            '<span class="text-success">C:\\Users\\mincho></span>'
        ],
        deb: [
            '<span class="text-success">mincho@debian:</span>$ sudo apt install python3-numpy',
            'Leyendo lista de paquetes...',
            'Instalando python3-numpy...',
            '<span class="text-success">mincho@debian:</span>$'
        ]
    },
    matplotlib: {
        win: [
            '<span class="text-success">C:\\Users\\mincho></span> pip install matplotlib',
            'Collecting matplotlib...',
            'Successfully installed matplotlib',
            '<span class="text-success">C:\\Users\\mincho></span>'
        ],
        deb: [
            '<span class="text-success">mincho@debian:</span>$ sudo apt install python3-matplotlib',
            'Leyendo lista de paquetes...',
            'Instalando python3-matplotlib...',
            '<span class="text-success">mincho@debian:</span>$'
        ]
    },
    sympy: {
        win: [
            '<span class="text-success">C:\\Users\\mincho></span> pip install sympy',
            'Collecting sympy...',
            'Successfully installed sympy',
            '<span class="text-success">C:\\Users\\mincho></span>>'
        ],
        deb: [
            '<span class="text-success">mincho@debian:</span>$ sudo apt install python3-sympy',
            'Leyendo lista de paquetes...',
            'Instalando python3-sympy...',
            '<span class="text-success">mincho@debian:</span>$'
        ]
    },
    django: {
        win: [
            '<span class="text-success">C:\\Users\\mincho></span> pip install django',
            'Collecting django...',
            'Successfully installed django',
            '<span class="text-success">C:\\Users\\mincho></span>'
        ],
        deb: [
            '<span class="text-success">mincho@debian:</span>$ sudo apt install python3-django',
            'Leyendo lista de paquetes...',
            'Instalando python3-django...',
            '<span class="text-success">mincho@debian:</span>$'
        ]
    }
};

// Función para animar terminal
function animateTerminal(elementId, lines, speed = 30) {
    const terminal = document.getElementById(elementId);
    let i = 0, currentLine = 0;
    let output = '';

    function type() {
        if (currentLine < lines.length) {
            if (i <= lines[currentLine].length) {
                output = lines.slice(0, currentLine).join('<br>') +
                    (currentLine > 0 ? '<br>' : '') +
                    lines[currentLine].substring(0, i) + '<span class="cursor"></span>';
                terminal.innerHTML = output;
                i++;
                setTimeout(type, speed);
            } else {
                currentLine++;
                i = 0;
                setTimeout(type, speed * 5);
            }
        } else {
            terminal.innerHTML = lines.join('<br>');
        }
    }
    type();
}

// Iniciar animaciones
window.onload = function () {
    // Python
    animateTerminal('terminal-python-win', commands.python.win);
    animateTerminal('terminal-python-deb', commands.python.deb);

    // Otras herramientas con retraso
    setTimeout(() => {
        animateTerminal('terminal-numpy-win', commands.numpy.win);
        animateTerminal('terminal-numpy-deb', commands.numpy.deb);
    }, 2000);

    setTimeout(() => {
        animateTerminal('terminal-matplotlib-win', commands.matplotlib.win);
        animateTerminal('terminal-matplotlib-deb', commands.matplotlib.deb);
    }, 4000);

    setTimeout(() => {
        animateTerminal('terminal-sympy-win', commands.sympy.win);
        animateTerminal('terminal-sympy-deb', commands.sympy.deb);
    }, 6000);

    setTimeout(() => {
        animateTerminal('terminal-django-win', commands.django.win);
        animateTerminal('terminal-django-deb', commands.django.deb);
    }, 8000);
};