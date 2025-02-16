from django import forms
from inicio.models import Receta

class CrearReceta(forms.Form):
    titulo = forms.CharField(
        max_length=40,
        widget=forms.TextInput(attrs={
            'class': 'form-control text-white',
            'placeholder': 'Título de la receta',
            'style': 'background-color: rgba(0, 0, 0, 0.5); color: white; border: 1px solid black;'
        })
    )
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control text-white',
            'placeholder': 'Descripción',
            'rows': 4,
            'style': 'background-color: rgba(0, 0, 0, 0.5); color: white; border: 1px solid black;'
        })
    )
    ingredientes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control text-white',
            'placeholder': 'Ingredientes',
            'rows': 4,
            'style': 'background-color: rgba(0, 0, 0, 0.5); color: white; border: 1px solid black;'
        })
    )
    pasos = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control text-white',
            'placeholder': 'Pasos a seguir',
            'rows': 4,
            'style': 'background-color: rgba(0, 0, 0, 0.5); color: white; border: 1px solid black;'
        })
    )
    tiempo_preparacion = forms.IntegerField(
        help_text="(Indica el tiempo de preparación en minutos)",
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control text-white',
            'placeholder': 'Tiempo de preparación (min)',
            'type': 'number',
            'style': 'background-color: rgba(0, 0, 0, 0.5); color: white; border: 1px solid black;'
        })
    )
    imagen = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control text-white',
            'style': 'background-color: rgba(0, 0, 0, 0.5); color: white; border: 1px solid black;'
        })
    )

class BuscarReceta(forms.Form):
    titulo = forms.CharField(
        max_length=40,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control text-white',
            'placeholder': 'Buscar por título',
            'style': 'background-color: rgba(0, 0, 0, 0.5); color: white; border: 1px solid black;'
        })
    )