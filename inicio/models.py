from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.

class Receta(models.Model):
    titulo = models.CharField(max_length=60)
    descripcion = models.TextField(max_length=3500)
    ingredientes = models.TextField(max_length=3500)
    pasos = models.TextField(max_length=3500)
    fecha_creacion = models.DateField(auto_now_add=True)
    tiempo_preparacion = models.IntegerField(help_text="Indica el tiempo de preparación en minutos.", 
                                             blank=True,
                                             null=True,
                                             validators=[MinValueValidator(1)])
    imagen = models.ImageField(upload_to='recetas/', blank=True, null=True) 

    def __str__(self):
        return f"{self.titulo} {self.descripcion}"

