from django.contrib import admin
from django.urls import path
from inicio.views import inicio, saludo

urlpatterns = [
    path('', inicio, name='inicio'),
    path('saludo/<str:nombre>/<str:apellido>/', saludo, name='saludo')
]
