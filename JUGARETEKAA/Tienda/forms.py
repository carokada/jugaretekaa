from django import forms
from .models import Producto


class FormProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'titulo', 
            'imagen', 
            'categoria', 
            'descripcion', 
            'precio',
        ]
        labels = {
            'titulo': "producto",
            'imagen': "imagen",
            'categoria': "categoria",
            'descripcion': "descripcion",
            'precio': "precio",
        }
        