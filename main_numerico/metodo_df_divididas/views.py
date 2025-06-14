from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def documentacion(request):
    return render(request, 'documentacion.html')

def menu(request):
    return render(request, 'menu.html')
