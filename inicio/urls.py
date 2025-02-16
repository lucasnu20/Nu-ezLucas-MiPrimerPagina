from django.contrib import admin
from django.urls import path
from inicio.views import inicio, crear_receta,listado_recetas, detalle_receta

urlpatterns = [
    path('', inicio, name='inicio'),
    path('crear-receta/', crear_receta, name='crear_receta'),
    path('listado-recetas/', listado_recetas, name='listado_recetas'),
    path('detalle-receta/<int:receta_id>',detalle_receta, name='detalle_receta')
]
