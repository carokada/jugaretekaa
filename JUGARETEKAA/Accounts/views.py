from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroUsuarioForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Usuario {username} creado exitosamente!')
            return redirect('tienda:index')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'accounts/register.html', {"form": form})