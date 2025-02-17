from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from inicio.models import Receta
from inicio.forms import CrearReceta, BuscarReceta, CreacionUsuarios
# Create your views here.

@never_cache
def inicio(request):
    return render(request, 'inicio/inicio.html')

@login_required
@never_cache
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

@never_cache
def listado_recetas(request):
    recetas = Receta.objects.all()
    formulario = BuscarReceta(request.GET,request.FILES)
    if formulario.is_valid():
        receta_buscada = formulario.cleaned_data.get("titulo")
        recetas = Receta.objects.filter(titulo__icontains=receta_buscada)
        
    return render(request, 'inicio/listado_recetas.html',{'recetas':recetas,'formulario':formulario})

@never_cache
def detalle_receta(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)
    return render(request, 'inicio/detalle_receta.html', {'receta': receta})

@never_cache
def contacto(request):
    return render(request, 'inicio/contacto.html')


def registrarse(request):
    if request.method == 'POST':
        form = CreacionUsuarios(request.POST)
        print(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')  # Redirigir a la página de inicio o alguna página personalizada
    else:
        form = CreacionUsuarios()

    return render(request, 'inicio/registro.html', {'form': form})
