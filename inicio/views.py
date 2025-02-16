from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
from django.utils import timezone
from inicio.models import Receta
from inicio.forms import CrearReceta, BuscarReceta
# Create your views here.

def inicio(request):
    return render(request, 'inicio/inicio.html')

def crear_receta(request):
    formulario = CrearReceta()

    if request.method == "POST":
        formulario = CrearReceta(request.POST,request.FILES)

        if formulario.is_valid():

            titulo = formulario.cleaned_data.get("titulo")
            descripcion = formulario.cleaned_data.get("descripcion")
            ingredientes = formulario.cleaned_data.get("ingredientes")
            pasos = formulario.cleaned_data.get("pasos")
            fecha_creacion = formulario.cleaned_data.get("fecha_creacion")
            tiempo_preparacion = formulario.cleaned_data.get("tiempo_preparacion")
            imagen = formulario.cleaned_data.get("imagen")
  
            receta = Receta(titulo=titulo,
                            ingredientes=ingredientes,
                            descripcion=descripcion,
                            pasos=pasos,
                            fecha_creacion=fecha_creacion,
                            tiempo_preparacion=tiempo_preparacion,
                            imagen=imagen)
            receta.save()
            return redirect("listado_recetas")
    return render(request, 'inicio/crear_recetas.html',{"formulario":formulario})

def listado_recetas(request):
    recetas = Receta.objects.all()
    formulario = BuscarReceta(request.GET,request.FILES)
    if formulario.is_valid():
        receta_buscada = formulario.cleaned_data.get("titulo")
        recetas = Receta.objects.filter(titulo__icontains=receta_buscada)
        
    return render(request, 'inicio/listado_recetas.html',{'recetas':recetas,'formulario':formulario})

def detalle_receta(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)
    return render(request, 'inicio/detalle_receta.html', {'receta': receta})