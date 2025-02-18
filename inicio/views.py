from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from inicio.models import Receta
from inicio.forms import CrearReceta, BuscarReceta, CustomUserCreationForm

# Create your views here.

def inicio(request):
    return render(request, 'inicio/inicio.html')

@login_required
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


def contacto(request):
    return render(request, 'inicio/contacto.html')


def register(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)

        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            
            login(request, user)
            return redirect(to="inicio")
        
        data["form"] = formulario

    return render(request, 'registration/register.html', data)

def exit(request):
    logout(request)
    return redirect('inicio')

