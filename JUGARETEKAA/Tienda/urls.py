from django.urls import path
from . import views

app_name = "tienda"
urlpatterns = [
    #leave empty string for base url
    path('', views.index, name="index"),
    path('categoria/<int:categoria_id>', views.filtro_categorias, name="filtro_categorias"),

    path('acerca/', views.acerca, name="acerca"),
    path('contacto/', views.contacto, name="contacto"),
    path('buscar/', views.buscar, name="buscar"),
    
    path('producto/<int:producto_id>', views.ver_producto, name="producto"),
    path('agregar/', views.agregar_producto, name="agregar"),
    path('editar/<int:producto_id>', views.editar_producto, name="editar"),
    path('eliminar/<int:producto_id>', views.eliminar_producto, name="eliminar"),
    
    path('carrito/<int:carrito_id>', views.ver_carrito, name="carrito"),
    path('carrito/<int:carrito_id>', views.agregar_al_carrito, name="carrito_add"),
]