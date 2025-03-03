from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as django_login
from usuarios.forms import CrearUsuarioForm, EditarUsuarioForm, UbicacionUserForm
from inicio.forms import BuscarReceta
from django.contrib.auth.views import PasswordChangeView, LogoutView
from django.urls import reverse_lazy
from usuarios.models import InfoUsuario, Provincia, UbicacionUser
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib import messages
from inicio.models import Receta


@method_decorator([never_cache], name='dispatch')
class Deslogueo(LogoutView):
    template_name = 'usuarios/logout.html'

@method_decorator([login_required, never_cache], name='dispatch')
class CambioPassword(PasswordChangeView):
    template_name = 'usuarios/cambio_pass.html'
    success_url = reverse_lazy('inicio')

    def form_valid(self, form):
        messages.success(self.request, "Tu contraseña ha sido cambiada exitosamente.")
        return super().form_valid(form)
    
@never_cache
def login(request):
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            
            django_login(request, usuario)
            
            InfoUsuario.objects.get_or_create(user=usuario)
            
            return redirect('inicio')
        else:
             form.errors.clear()
             form.add_error(None, "Usuario o contraseña incorrectos.") 
    else:
        form = AuthenticationForm()
       
        
    print(f'Errores formulario: {form.errors}')


    return render(request, 'usuarios/login.html', {'form': form})


@never_cache
def registro(request):
    
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('login')
    else:
        form = CrearUsuarioForm()
    
    return render(request, 'usuarios/registro.html', {'form': form})

@never_cache
@login_required
def editar_perfil(request):
    info_usuario = request.user.infousuario
    ubicacion, _ = UbicacionUser.objects.get_or_create(infousuario=info_usuario)

    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, request.FILES, instance=request.user)
        form_ubicacion = UbicacionUserForm(request.POST, instance=ubicacion)

        # Actualizar provincias según el país seleccionado
        print(f"post: {request.POST}")
        pais_id = request.POST.get('pais')
        if pais_id:
            form_ubicacion.fields['provincia'].queryset = Provincia.objects.filter(pais_id=pais_id)

        if form.is_valid() and form_ubicacion.is_valid():

            # Manejo de la foto de perfil
            foto_perfil = form.cleaned_data.get('foto_perfil')
            if form.cleaned_data.get('eliminar_foto') and info_usuario.foto_perfil:
                info_usuario.foto_perfil.delete(save=False)
                info_usuario.foto_perfil = None
            elif foto_perfil:
                info_usuario.foto_perfil = foto_perfil

            # Actualizo con los cleaned data para datos de usuario y ubicación 
            for campo in ['fecha_nacimiento', 'telefono', 'detalle_perfil', 'intereses_culinarios']:
                setattr(info_usuario, campo, form.cleaned_data.get(campo) or getattr(info_usuario, campo))

            for campo in ['pais', 'provincia', 'ciudad']:
                setattr(ubicacion, campo, form_ubicacion.cleaned_data.get(campo) or getattr(ubicacion, campo))

            info_usuario.save()
            ubicacion.save()
            form.save()
            form_ubicacion.save()

            messages.success(request, "Perfil actualizado correctamente.")
            return redirect('ver_perfil')
        else:
            messages.error(request, "Hubo un error al actualizar el perfil.")

    else:
        form = EditarUsuarioForm(instance=request.user, initial={
            'foto_perfil': info_usuario.foto_perfil,
            'fecha_nacimiento': info_usuario.fecha_nacimiento.strftime('%Y-%m-%d') if info_usuario.fecha_nacimiento else '',
            'telefono': info_usuario.telefono,
            'detalle_perfil': info_usuario.detalle_perfil,
            'intereses_culinarios': info_usuario.intereses_culinarios,
        })
        form_ubicacion = UbicacionUserForm(instance=ubicacion)

    return render(request, 'usuarios/editar_perfil.html', {'form': form, 'form_ubicacion': form_ubicacion})



@never_cache
@login_required
def ver_perfil(request):
    info_usuario = request.user.infousuario
    ubicacion, _ = UbicacionUser.objects.get_or_create(infousuario=info_usuario)

    contexto = {
        "usuario": request.user,
        "info_usuario": info_usuario,
        "ubicacion": ubicacion,
    }
    
    return render(request, "usuarios/ver_perfil.html", contexto)

def obtener_provincias(request):

    pais_id = request.GET.get("pais_id")
    print(f"pais: {pais_id}")
    if pais_id:
        provincias = Provincia.objects.filter(pais_id=pais_id).values("id", "nombre")
        return JsonResponse(list(provincias), safe=False)
    return JsonResponse([], safe=False)


def recetas_usuario(request, user_id):
    recetas = Receta.objects.filter(usuario_id=user_id)
    formulario = BuscarReceta(request.GET, request.FILES)
    if formulario.is_valid():
        receta_buscada = formulario.cleaned_data.get("titulo")
        recetas = Receta.objects.filter(titulo__icontains=receta_buscada, usuario_id=user_id)
    return render(request, 'usuarios/mis_recetas.html', {'recetas': recetas, 'formulario': formulario})