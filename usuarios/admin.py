from django.contrib import admin
from .models import User, InfoUsuario, UbicacionUser, Provincia, Pais

# Register your models here.
admin.site.register(InfoUsuario)
admin.site.register(UbicacionUser)
admin.site.register(Provincia)
admin.site.register(Pais)