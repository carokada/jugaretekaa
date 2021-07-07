from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from .forms import FormProducto
from .models import Carrito, Categoria, Producto


# Create your views here.

    # main
def index(request):
    
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    #ultimos_productos = Producto.objects.order_by('_pub_date')[:5]
    
    if "agregar_al_carrito" not in request.session:
        request.session["agregar_al_carrito"] = []

    context = {
        "productos": productos,
        "categorias": categorias,
        "agregar_al_carrito": request.session["agregar_al_carrito"],
        #"ultimos_productos": ultimos_productos,
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
@permission_required('Tienda.add_producto')
def agregar_producto(request):
    
    categorias = Categoria.objects.all()

    if request.method == "POST":
        form = FormProducto(request.POST, request.FILES, instance=Producto(imagen=request.FILES['image']))
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
@permission_required('Tienda.change_producto')
def editar_producto(request, producto_id):

    categorias = Categoria.objects.all()
    un_producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        form = FormProducto(data=request.POST, files=request.FILES, instance=Producto(imagen=request.FILES, instance = un_producto))
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
@permission_required('Tienda.delete_producto')
def eliminar_producto(request, producto_id):

    un_producto = get_object_or_404(Producto, id=producto_id)
    un_producto.delete()
    return redirect("tienda:index")


    # carrito
@login_required(login_url='usuario:login')
@permission_required('Tienda.view_carrito')
def carrito(request, carrito_id):

    categorias = Categoria.objects.all()
    mi_carrito = get_object_or_404(Carrito, pk=carrito_id)
    if mi_carrito is None:
        mi_carrito = Carrito.get_carrito(usuario=request.user)
        if User.is_authenticated:

            items = mi_carrito.lista_productos.all()
            context = {
                "categorias": categorias,
                "mi_carrito": mi_carrito,
                "items": items,
            }
            return render(request, 'tienda/carrito.html', context)
    else:
        items = mi_carrito.lista_productos.all()
        context = {
            "categorias": categorias,
            "carrito": mi_carrito,
            "items": items,
        }
    return render(request, 'tienda/carrito.html', context)


@login_required(login_url='usuario:login')
@permission_required('Tienda.add_carrito')
def agregar_al_carrito(request, producto_id):

    item = get_object_or_404(Producto, pk=producto_id)
    mi_carrito, create= Carrito.objects.get_or_create(usuario=request.user)
    if Carrito.objects.filter(usuario=request.user):
        print("agregando al carrito")
        mi_carrito.lista_productos.add(item)
        mi_carrito.save()
        print("producto agregado")
        return HttpResponseRedirect(reverse('tienda:carrito', args=(mi_carrito.id,))) 
    else:
        mi_carrito = Carrito.get_carrito()
        mi_carrito.lista_productos.add(item)
        mi_carrito.save()
        return HttpResponseRedirect(reverse('tienda:carrito', args=(mi_carrito.id,)))


@login_required(login_url='usuario:login')
@permission_required('Tienda.delete_carrito')
def carrito_eliminar(request, carrito_id):

    mi_carrito = get_object_or_404(Carrito, id=carrito_id)
    mi_carrito.delete()
    messages.warning(request, f'Usted ha borrado su carrito')
    return redirect("sitio:index")
