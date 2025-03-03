from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User
from .models import Provincia, UbicacionUser
from usuarios.validators import phone_number_validator

class CrearUsuarioForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repetir Contraseña', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {field: '' for field in fields}
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email
        
class EditarUsuarioForm(UserChangeForm):
    password = None
    email = forms.EmailField()
    first_name = forms.CharField(label='Nombre')
    last_name = forms.CharField(label='Apellido')
    foto_perfil = forms.ImageField(required=False)
    fecha_nacimiento = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d', '%d/%m/%Y'])
    telefono = forms.CharField(max_length=15, required=False, validators=[phone_number_validator])
    detalle_perfil = forms.CharField(max_length=2000, required=False)
    intereses_culinarios = forms.CharField(max_length=2000, required=False)
    eliminar_foto = forms.BooleanField(
        required=False,  # No es obligatorio marcarlo
        initial=False,   # Por defecto, no está marcado
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'foto_perfil', 'fecha_nacimiento', 'telefono','detalle_perfil', 'intereses_culinarios']

  
    
class UbicacionUserForm(forms.ModelForm):
    class Meta:
        model = UbicacionUser
        fields = ["pais", "provincia", "ciudad"]

    def __init__(self, *args, **kwargs):
        super(UbicacionUserForm, self).__init__(*args, **kwargs)

        instance = kwargs.get("instance")
        data = kwargs.get("data")  

        if data and "pais" in data:
            try:
                pais_id = int(data.get("pais"))
                self.fields["provincia"].queryset = Provincia.objects.filter(pais_id=pais_id)
            except ValueError:
                self.fields["provincia"].queryset = Provincia.objects.none()
        elif instance and instance.pais:
            self.fields["provincia"].queryset = Provincia.objects.filter(pais=instance.pais)
        else:
            self.fields["provincia"].queryset = Provincia.objects.none()

        if instance and instance.provincia:
            self.fields["provincia"].queryset |= Provincia.objects.filter(id=instance.provincia.id)

        

    