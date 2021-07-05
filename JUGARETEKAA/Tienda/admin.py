from .models import Categoria, Producto, Carrito
from django.contrib import admin

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Carrito)