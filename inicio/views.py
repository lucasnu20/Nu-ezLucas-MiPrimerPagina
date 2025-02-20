from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from inicio.models import Receta
from inicio.forms import CrearReceta, BuscarReceta, CustomUserCreationForm  
from django.views.generic.edit import UpdateView,DeleteView
from django.urls import reverse_lazy
from django import forms



class ModificarRecetaView(UpdateView):
    model = Receta
    fields = '__all__' 
    template_name = 'inicio/CBV/modificar_recetas.html'
    success_url = reverse_lazy('listado_recetas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Función auxiliar para actualizar el estilo de los atributos comunes
        def actualizar_widgets(campo, placeholder=None):
            campo.field.widget.attrs.update({
                'class': 'form-control text-white',
                'style': 'background-color: rgba(0, 0, 0, 0.5); color: white; border: 1px solid black;'
            })
            if placeholder:
                campo.field.widget.attrs.update({
                    'placeholder': placeholder
                })

        # Actualizar los widgets de los campos comunes
        for field in context['form']:
            # Campos comunes todos menos tiempo_preparacion
            if isinstance(field.field, (forms.CharField, forms.Textarea, forms.ImageField)):
                #  asignamos el placeholder para cada campo
                if field.name == 'titulo':
                    actualizar_widgets(field, placeholder="Título de la receta")
                elif field.name == 'descripcion':
                    actualizar_widgets(field, placeholder="Descripción")
                elif field.name == 'ingredientes':
                    actualizar_widgets(field, placeholder="Ingredientes")
                elif field.name == 'pasos':
                    actualizar_widgets(field, placeholder="Pasos a seguir")
                elif field.name == 'imagen':
                    actualizar_widgets(field)  # No requiere placeholder
            # Para el campo tiempo_preparacion es diferente
            elif isinstance(field.field, forms.IntegerField):
                actualizar_widgets(field, placeholder="Tiempo de preparación (min)")

        return context

class EliminarRecetaView(DeleteView):
    model = Receta
    fields = '__all__'
    template_name = 'inicio/CBV/eliminar_recetas.html'
    context_object_name = 'receta'
    success_url = reverse_lazy('listado_recetas')

# Create your views here.
@never_cache
def inicio(request):
    return render(request, 'inicio/inicio.html')

@login_required
def crear_receta(request):
    form = CrearReceta()

    if request.method == "POST":
        form = CrearReceta(request.POST,request.FILES)

        if form.is_valid():

            titulo = form.cleaned_data.get("titulo")
            descripcion = form.cleaned_data.get("descripcion")
            ingredientes = form.cleaned_data.get("ingredientes")
            pasos = form.cleaned_data.get("pasos")
            fecha_creacion = form.cleaned_data.get("fecha_creacion")
            tiempo_preparacion = form.cleaned_data.get("tiempo_preparacion")
            imagen = form.cleaned_data.get("imagen")
  
            receta = Receta(titulo=titulo,
                            ingredientes=ingredientes,
                            descripcion=descripcion,
                            pasos=pasos,
                            fecha_creacion=fecha_creacion,
                            tiempo_preparacion=tiempo_preparacion,
                            imagen=imagen)
            receta.save()
            return redirect("listado_recetas")
    return render(request, 'inicio/crear_recetas.html',{"form":form})

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

@never_cache
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

@never_cache
def exit(request):
    logout(request)
    return redirect('inicio')


