from .forms import RegistroUsuarioForm
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def loginpage(request):
    if request.user.is_authenticated:
        return redirect('tienda:index')
    else: 
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, usename=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('tienda:index')
            else:
                messages.info(request, 'Usuario o contrasena incorrectos.')

        context = {}
        return render(request, 'usuario/login.html', context)


@login_required(login_url='usuario:login')
def logoutpage(request):

    logout(request)
    return redirect('tienda:index')
    


def registro(request):
    if request.user.is_authenticated:
        return redirect('tienda:index')
    else:
        form = RegistroUsuarioForm()

        if request.method == 'POST':
            form = RegistroUsuarioForm(request.POST)
            if form.is_valid():
                form.save()
                user=form.cleaned_data.get('username')
                messages.success(request, 'Usuario'+ user +'creado exitosamente')

                return redirect('login')

        context = {
            "form": form
        }
        return render(request, 'usuario/registro.html', context)