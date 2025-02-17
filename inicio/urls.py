from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from inicio.views import inicio, crear_receta,listado_recetas, detalle_receta,contacto,registrarse

urlpatterns = [
    path('', inicio, name='inicio'),
    path('crear-receta/', crear_receta, name='crear_receta'),
    path('listado-recetas/', listado_recetas, name='listado_recetas'),
    path('detalle-receta/<int:receta_id>',detalle_receta, name='detalle_receta'),
    path('contacto/',contacto, name='contacto'),
    path('registro/', registrarse, name='registro'),
    path('login/', LoginView.as_view(template_name='inicio/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='inicio'), name='logout'),

]
