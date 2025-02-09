from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

# Create your views here.

def inicio(request):
    #return HttpResponse("<h1>Hola soy la vista</h1>")
    return render(request, 'inicio/inicio.html')

def saludo(request,nombre,apellido):
    hora_actual = datetime.now()
    # el diccionario que se pasa en el render se llama "contexto" eso se pasa al template como parametro
    return render(request, 'inicio/saludo.html',{'hora':hora_actual,'nombre':nombre,'apellido':apellido})