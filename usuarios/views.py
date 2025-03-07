from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login as django_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView, LogoutView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from usuarios.forms import CrearUsuarioForm, EditarUsuarioForm, UbicacionUserForm
from inicio.forms import BuscarReceta
from inicio.models import Receta
from django.http import JsonResponse
from usuarios.models import InfoUsuario, Provincia, UbicacionUser
from django.views.generic import DetailView
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.db.models import Count


class PerfilUsuarioView(DetailView):
    model = User
    template_name = 'usuarios/perfil_usuario.html'
    context_object_name = 'perfil_usuario'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener InfoUsuario basado en user_id
        info_usuario = InfoUsuario.objects.filter(user_id=self.object.id).first()
        context['info_usuario'] = info_usuario

        # Obtener UbicacionUser basado en infousuario_id
        if info_usuario:
            context['ubicacion_usuario'] = UbicacionUser.objects.filter(infousuario_id=info_usuario.id).first()
        else:
            context['ubicacion_usuario'] = None

        # Obtener recetas creadas por el usuario
        recetas_usuario = Receta.objects.filter(usuario_id=self.object.id)
        context['recetas_usuario'] = recetas_usuario

        return context


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
                valor = form.cleaned_data.get(campo)
                setattr(info_usuario, campo, valor if valor != "" else None)

            for campo in ['pais', 'provincia', 'ciudad']:
                valor = form_ubicacion.cleaned_data.get(campo)
                setattr(ubicacion, campo, valor if valor != "" else None)

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


@never_cache
@login_required
def recetas_usuario(request, user_id):
    recetas = Receta.objects.filter(usuario_id=user_id)
    formulario = BuscarReceta(request.GET, request.FILES)
    if formulario.is_valid():
        receta_buscada = formulario.cleaned_data.get("titulo")
        recetas = Receta.objects.filter(titulo__icontains=receta_buscada, usuario_id=user_id)
    return render(request, 'usuarios/mis_recetas.html', {'recetas': recetas, 'formulario': formulario})

@never_cache
@login_required
def buscar_usuarios(request):
    busqueda_del_usuario = request.GET.get('q', '')  # Valor del campo de búsqueda
    usuarios = User.objects.filter(username__icontains=busqueda_del_usuario).select_related(
        "infousuario__ubicacion__provincia"
    ).annotate(num_recetas=Count('recetas'))


    return render(request, 'usuarios/buscar_usuarios.html', {'usuarios': usuarios, 'busqueda': busqueda_del_usuario})