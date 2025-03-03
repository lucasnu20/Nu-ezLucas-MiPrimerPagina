from django.core.exceptions import ValidationError
import re

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password):
            raise ValidationError("La contraseña debe contener al menos una letra mayúscula.")
        if not re.search(r'\d', password):
            raise ValidationError("La contraseña debe contener al menos un número.")

    def get_help_text(self):
        return "Tu contraseña debe contener al menos una letra mayúscula y un número."
    
def no_spaces_validator(value):
    if " " in value:
        raise ValidationError("Este campo no puede contener espacios.")
    
def phone_number_validator(value):
    if not re.match(r'^\+?\d{7,15}$', value):  
        raise ValidationError("Ingrese un número de teléfono válido (7-15 dígitos, opcionalmente con + al inicio).")