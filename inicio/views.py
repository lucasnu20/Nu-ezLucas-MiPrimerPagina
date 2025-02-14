from django.shortcuts import render,redirect
from django.http import HttpResponse
from datetime import datetime
from inicio.models import Producto, Pedido
from inicio.forms import CrearProducto, BuscarProducto
# Create your views here.

def inicio(request):
    #return HttpResponse("<h1>Hola soy la vista</h1>")
    return render(request, 'inicio/inicio.html')

def crear_producto(request):
    formulario = CrearProducto()
    
    if request.method == "POST":
        formulario = CrearProducto(request.POST)
        if formulario.is_valid():
            nombre = formulario.cleaned_data.get("nombre")
            precio = formulario.cleaned_data.get("precio")
            descripcion = formulario.cleaned_data.get("descripcion")
            producto = Producto(nombre=nombre, precio=precio, descripcion=descripcion)
            producto.save()
            return redirect("listado_productos")
    return render(request, 'inicio/crear_producto.html',{"formulario":formulario})

def listado_productos(request):
    productos = Producto.objects.all()
    formulario = BuscarProducto(request.GET)
    if formulario.is_valid():
        producto_buscado = formulario.cleaned_data.get("nombre")
        productos = Producto.objects.filter(nombre__icontains=producto_buscado)
        
    return render(request, 'inicio/listado_productos.html',{'productos':productos,'formulario':formulario})


def crear_pedido(request):
    return render(request, 'inicio/crear_pedido.html')