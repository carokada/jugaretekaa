from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistroUsuarioForm (UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2',
        ]
        labels = {
            'first_name': "Nombre",
            'last_name': "Apellidos",
            'email': "Correo electronico",
            'username': "Nombre de Usuario",
            'password1': "Contrasena",
            'password2': "Repetir Contrasena",
        }