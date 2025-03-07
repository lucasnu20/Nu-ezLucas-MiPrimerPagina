from django.urls import path
from usuarios.views import login, registro, editar_perfil, CambioPassword,obtener_provincias, ver_perfil, recetas_usuario, PerfilUsuarioView, buscar_usuarios
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registro/', registro, name='registro'),
    path('editar-perfil/', editar_perfil, name='editar_perfil'),
    path('editar-perfil/cambiar-pass/', CambioPassword.as_view(), name='cambiar_pass'),
    path("perfil/", ver_perfil, name="ver_perfil"),
    path('editar-perfil/obtener-provincias/', obtener_provincias, name='obtener_provincias'),
    path('mis-recetas/<int:user_id>/', recetas_usuario, name='mis_recetas'),
    path('usuarios/perfil/<int:pk>/', PerfilUsuarioView.as_view(), name='perfil_usuario'),
    path('buscar/', buscar_usuarios, name='buscar_usuarios'),

]