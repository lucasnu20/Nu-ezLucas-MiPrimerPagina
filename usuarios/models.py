from django.db import models
from django.contrib.auth.models import User
import os
 
def user_directory_path(instance, filename):
    """Devuelve la ruta de la imagen de perfil del usuario."""
    return f'usuarios/{instance.user.username}/{filename}'

def default_profile_image():
    """Devuelve la ruta de la imagen de perfil por defecto."""
    return "static/images/profile.webp"

class Pais(models.Model):
    nombre = models.CharField(max_length=100, unique=True)  # El nombre del país

    def __str__(self):
        return self.nombre
    
class Provincia(models.Model):
    nombre = models.CharField(max_length=100)  # El nombre de la provincia
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='provincias')  # Relación con el modelo Pais

    def __str__(self):
        return f'{self.nombre}, {self.pais.nombre}'


class InfoUsuario(models.Model):    
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    foto_perfil = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    detalle_perfil = models.TextField(max_length=2000, null=True, blank=True)
    intereses_culinarios = models.TextField(max_length=2000, null=True, blank=True)

    def delete_old_image(self):
        """Elimina la imagen anterior si existe antes de subir una nueva."""
        if self.pk:  # Verifica que la instancia ya existe en la BD
            try:
                old_instance = InfoUsuario.objects.get(pk=self.pk)
                if old_instance.foto_perfil and old_instance.foto_perfil != self.foto_perfil:
                    if os.path.isfile(old_instance.foto_perfil.path):  # Verifica que el archivo existe
                        os.remove(old_instance.foto_perfil.path)  # Elimina la imagen anterior
            except InfoUsuario.DoesNotExist:
                pass  # Si el usuario no existe aún, no hace nada

    def save(self, *args, **kwargs):
        self.delete_old_image()  # Llama a la función antes de guardar
        super().save(*args, **kwargs)  # Guarda la nueva imagen


class UbicacionUser(models.Model):
    infousuario = models.OneToOneField(InfoUsuario, on_delete=models.CASCADE, related_name="ubicacion")
    pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True, blank=True, related_name='ubicaciones')
    provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True, blank=True, related_name='ubicaciones')
    ciudad = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.infousuario.user.username} - {self.pais} - {self.provincia} - {self.ciudad}"