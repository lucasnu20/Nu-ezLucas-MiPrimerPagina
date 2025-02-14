from django import forms

class CrearProducto(forms.Form):
    nombre = forms.CharField(max_length=40)
    precio = forms.DecimalField(max_digits=10, decimal_places=2)
    descripcion = forms.CharField(widget=forms.Textarea, required=False)
    
class BuscarProducto(forms.Form):
    nombre = forms.CharField(max_length=40, required=False) # Se pone en false porque puede ser que no se utilice filtro de busqueda
    