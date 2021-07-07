from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Categoria(models.Model):
    descripcion = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.descripcion}"

class Producto(models.Model):
    titulo = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='images/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, blank=True, null=True, related_name="categoria")
    descripcion = models.CharField(max_length=2000)
    precio = models.IntegerField()
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"id#{self.id}: {self.titulo} - ${self.precio}"
        
    @property
    def imageURL(self):
        try:
            url = self.imagen.url
        except:
            url = ''
        return url

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    lista_productos = models.ManyToManyField(Producto, blank=True, related_name="productos_carrito")
    total_carrito = models.IntegerField(null=True, blank=True)
    fecha_orden = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"el usuario {self.usuario} ha enviado una orden de compra id#{self.id}."
    
    def get_carrito(self):
        return self.create(ususario=User)

    def get_total(self):
        return sum([item.product.price for item in self.lista_productos.all()])


