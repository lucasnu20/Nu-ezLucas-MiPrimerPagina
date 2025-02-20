from django import forms 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User 
from django.core.exceptions import ValidationError

class CrearReceta(forms.Form):
    titulo = forms.CharField(
        max_length=60,
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

# pruebas de validaciones pero no se encontro una solucion definitiva, se comenta por el momento
'''    def clean_titulo(self):
        titulo = self.cleaned_data['titulo']
        if len(titulo) > 60:
            raise ValidationError("El título no puede tener más de 60 caracteres.")
        return titulo

    def clean_descripcion(self):
        descripcion = self.cleaned_data['descripcion']
        if len(descripcion) > 3500:
            raise ValidationError("La descripción no puede tener más de 3500 caracteres.")
        return descripcion
    
    def clean_ingredientes(self):
        descripcion = self.cleaned_data['descripcion']
        if len(descripcion) > 3500:
            raise ValidationError("Los ingredientes no pueden tener más de 3500 caracteres.")
        return descripcion
    
    def clean_pasos(self):
        descripcion = self.cleaned_data['descripcion']
        if len(descripcion) > 3500:
            raise ValidationError("El paso a paso no puede tener más de 3500 caracteres.")
        return descripcion'''

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

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username
    