const terminal = document.getElementById('terminal');
const cursor = document.getElementById('cursor');

const lines = [
    '<span class="text-success">mincho@debian</span>:~$ sudo apt update',
    'Obteniendo paquetes... Hecho',
    '<span class="text-success">mincho@debian</span>:~$ sudo apt install python3',
    'Instalando dependencias de Análisis Numérico...',
    'Descargando paquetes... Hecho',
    'Configurando python3... Listo',
    '<span class="text-success">mincho@debian</span>:~$ python3 --version',
    'Somos UES!!!!',
    '<span class="text-success">mincho@debian</span>:~$'
];

let currentLine = 0;
let currentChar = 0;
let outputLines = [];

function typeLine() {
    if (currentLine >= lines.length) return;

    const line = lines[currentLine];
    currentChar++;

    const typedPart = line.substring(0, currentChar);
    const tempLine = typedPart + '<span class="cursor" id="cursor"></span>';

    // Copiamos líneas anteriores y agregamos la línea actual con cursor
    const rendered = [...outputLines, tempLine].join('<br>');
    terminal.innerHTML = rendered;

    if (currentChar < line.length) {
        setTimeout(typeLine, 30);
    } else {
        outputLines.push(line); // guardar línea ya completa
        currentLine++;
        currentChar = 0;
        setTimeout(typeLine, 600);
    }
}

setTimeout(typeLine, 800);