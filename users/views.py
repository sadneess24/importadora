from django.shortcuts import render, redirect
from .forms import FormularioRegistro, FormularioEntrar
# Create your views here.
from django.contrib.auth import login, authenticate, logout
from sweetify import warning, success

# Create your views here.
def registrar(request):
    if request.method == 'POST':
        form = FormularioRegistro(data=request.POST)
        if form.is_valid():
            form.save()
            success(request, 'Usuario creado correctamente')
            return redirect('mostrar_principal')
        else:
            warning(request, 'Nombre de usuario y/o contraseña inválida')
    else:
        form = FormularioRegistro()

    context = {
        'form': form
    }
    return render(request, 'user/signup.html', context)

def entrar(request):
    if request.method == 'POST':
        datos_usuario = FormularioEntrar(data = request.POST)
        es_valido = datos_usuario.is_valid()
        if es_valido:
            usuario = authenticate(
                username = datos_usuario.cleaned_data['username'],
                password = datos_usuario.cleaned_data['password']
            )
            if usuario is not None:
                login(request, usuario)
                success(request, f'Bienvenido {usuario.username}')
                return redirect('mostrar_principal')
            
        warning(request, 'Usuario y contraseña invalidos')
        contexto = {
        'form': datos_usuario
        }
        return render(request,"user/login.html",contexto)
    else:
        context ={
            'form': FormularioEntrar()
        }
        return render(request,"user/login.html",context)
    
def exit(request):
    logout(request)
    success(request, 'Sesión cerrada correctamente')
    return redirect('mostrar_principal')