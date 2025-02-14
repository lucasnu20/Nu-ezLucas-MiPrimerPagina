from django.db import models

# Create your models here.

class Producto(models.Model):
    nombre = models.CharField(max_length=40)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.nombre}  ${self.precio}"

class Pedido(models.Model):
    numero_pedido = models.CharField(max_length=50, unique=True)
    fecha_pedido = models.DateField(auto_now_add=True)  # Establece la fecha al momento de la creación
    productos = models.ManyToManyField(Producto)  # Relación muchos a muchos con Producto
    
    def __str__(self):
        return f"Pedido #{self.numero_pedido} - {self.fecha_pedido}"