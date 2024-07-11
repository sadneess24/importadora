from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from sweetify import warning, success
from users.forms import FormularioEditar, FormularioRegistro

@login_required
@user_passes_test(lambda u: u.is_superuser)
def administrar_pagina(request):
    return render(request, 'admin/admin_users.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def administrar_usuarios(request):
    usuarios = User.objects.filter(is_superuser=False)
    context = {
        'titulo': 'Listado de usuarios',
        'usuarios': usuarios,
        'form': FormularioRegistro
    }
    return render(request, 'admin/admin_users.html', context)

#LISTAR USUARIOS
def listado(request):
    if request.user.is_authenticated and request.user.is_superuser:
        context = {
            'titulo': 'Listado de usuarios',
            'usuarios': User.objects.filter(is_superuser=False),
            'form': FormularioRegistro
        }
        return render(request, 'admin/admin_users.html', context)
    else:
        warning(request, 'No tienes permisos para acceder a esta página')
        return redirect('home')

#ELIMINAR USUARIO    
def eliminar(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        usuario = User.objects.get(id=id)
        usuario.delete()
        success(request, 'Usuario eliminado correctamente')
        return redirect('listado')
    else:
        warning(request, 'No tienes permisos para acceder a esta página')
        return redirect('home')

#EDITAR USUARIO
@login_required
@user_passes_test(lambda u: u.is_superuser)
def editar_usuario(request, id):
    usuario = User.objects.get(id=id)
    if request.method == 'POST':
        form = FormularioEditar(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            success(request, 'Usuario editado correctamente')
            return redirect('administrar_usuarios')
        else:
            warning(request, 'No se pudo editar el usuario')
    else:
        form = FormularioEditar(instance=usuario)
    context = {
        'usuario': usuario,
        'form': form
    }
    return render(request, 'admin/edit_user.html', context)
    
#CRUD PRODUCTOS


#Listar PRODUCTOS
