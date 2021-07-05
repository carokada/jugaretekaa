from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Carrito, Categoria, Producto
from .forms import FormProducto


# Create your views here.

    # main
def index(request):
    
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    
    if "agregar_al_carrito" not in request.session:
        request.session["agregar_al_carrito"] = []

    context = {
        "productos": productos,
        "categorias": categorias,
        "agregar_al_carrito": request.session["agregar_al_carrito"],
    }
    return render(request, 'tienda/index.html', context)


def filtro_categorias(request, categoria_id):
    
    categorias = Categoria.objects.all()
    una_categoria = get_object_or_404(Categoria, id=categoria_id)
    queryset = Producto.objects.all()
    queryset = queryset.filter(categoria=una_categoria)

    context = {
        "filtro_productos": queryset,
        "categorias": categorias,
        "categoria_seleccionada": una_categoria
    }
    return render(request, 'tienda/buscar.html', context)


def acerca(request):

    categorias = Categoria.objects.all()

    context = {
        "categorias": categorias,
    }
    return render(request, 'tienda/acerca.html', context)


def contacto(request):

    categorias = Categoria.objects.all()

    context = {
        "categorias": categorias,
    }
    return render(request, 'tienda/contacto.html', context)


def buscar(request):

    categorias = Categoria.objects.all()
    queryset = request.GET.get("buscar")
    if queryset:
        producto_buscar = Producto.objects.filter(
            Q(titulo__icontains = queryset) |
            Q(categoria__icontains = queryset) |
            Q(descripcion__icontains = queryset)
        ).distinct()

    context = {
        "producto_buscar": producto_buscar,
        "categorias": categorias,
        }
    return render(request, 'tienda/buscar.html', context)


    # productos
def ver_producto(request, producto_id):

    categorias = Categoria.objects.all()
    un_producto = get_object_or_404(Producto, id=producto_id)

    context = {
        "un_producto": un_producto,
        "categorias": categorias,
    }
    return render(request, 'tienda/producto.html', context)


@login_required(login_url='usuario:login')
def agregar_producto(request):
    
    categorias = Categoria.objects.all()

    if request.method == "POST":
        user = User.objects.get(username=request.user)
        form = FormProducto(request.POST, request.FILES, instance=Producto(imagen=request.FILES['imagen']))
        
        if form.is_valid():
            form.save()
            return redirect('tienda:index')
    else:
        form = FormProducto(initial={'fecha_agregado':timezone.now()})
        context = {
            "form": form,
            "categorias": categorias,
        }
        return render(request, 'tienda/agregar.html', context)


@login_required(login_url='usuario:login')
def editar_producto(request, producto_id):

    categorias = Categoria.objects.all()
    un_producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        form = FormProducto(request.POST, request.FILES, instance=Producto(imagen=request.FILES['imagen']))
        if form.is_valid():
            form.save()
            return redirect('tienda:index')
        else:
            form = FormProducto(instance=un_producto)
            context = {
                "un_producto": un_producto,
                "categorias": categorias,
                "form": form,
            }
            return render(request, 'tienda/editar.html', context)


@login_required(login_url='usuario:login')
def eliminar_producto(request, producto_id):

    un_producto = get_object_or_404(Producto, id=producto_id)
    un_producto.delete()
    return redirect("tienda:index")


    # carrito
def ver_carrito(request, carrito_id):

    categorias = Categoria.objects.all()
    user = User.objects.get(username=request.user)
    carrito = Carrito.objects.get(id=carrito_id)
    productos_carrito = Carrito.lista_productos.all()

    context = {
        "user": user,
        "carrito": carrito,
        "categorias": categorias,
        "productos_carrito": productos_carrito,
    }
    return render(request, 'tienda:carrito', context)

@login_required(login_url='usuario:login')
def agregar_al_carrito(request, carrito_id):

    if request.method == 'POST':
        carrito = Carrito.objects.get(id=carrito_id)
        producto_carrito_id = int(request.POST["productos"])
        producto_carrito = Producto.objects.get(pk=producto_carrito_id)
        producto_carrito.carrito.add(carrito)
        return HttpResponseRedirect(reverse('sitio:carrito', args=carrito_id))


#@login_required(login_url='usuario:login')
#def agregar_al_carrito(request, producto_id):
#    item_carrito = get_object_or_404(Producto, id=producto_id)
#    for id in request.session["agregar_al_carrito"]:
#        if id == producto_id:
#            return HttpResponseRedirect(reverse("sitio:producto", args=(item_carrito.id)))            
#    request.session["agregar_al_carrito"] += [item_carrito]
#     return HttpResponseRedirect(reverse("sitio:producto", args=(item_carrito.id)))

