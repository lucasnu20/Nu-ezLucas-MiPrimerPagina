from django.contrib import admin
from django.urls import path
from inicio.views import inicio, crear_pedido,crear_producto,listado_productos

urlpatterns = [
    path('', inicio, name='inicio'),
    path('crear-producto/', crear_producto, name='crear_producto'),
    path('crear-pedido/', crear_pedido, name='crear_pedido'),
    path('listado-productos/', listado_productos, name='listado_productos')
]
