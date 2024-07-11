from django.shortcuts import render, redirect
from .forms import *
from .models import *
from cart.views import _cart_id
from cart.models import *
from django.contrib import messages, auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import requests
# Create your views here.
def registro(request):
    if request.method == 'POST':
        form = RegistroFormulario(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Cuenta.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username,password=password)
            user.phone_number = phone_number
            user.save()
            messages.success(request, 'Registro completado')
            return redirect('registro')
    else:
        form = RegistroFormulario()
    contexto = {
        'form':form,
    }
    return render(request, 'auth/register.html', contexto)

def iniciar_sesion(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                carro = Carro.objects.get(cart_id=_cart_id(request))
                is_carro_item_exists = CarroItem.objects.filter(carro=carro).exists()
                if is_carro_item_exists:
                    carro_item = CarroItem.objects.filter(carro=carro)
                    producto_variacion = []

                    for item in carro_item:
                        variacion = item.variaciones.all()
                        producto_variacion.append(list(variacion))
                    
                    carro_item = CarroItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in carro_item:
                        variacion_existe = item.variaciones.all()
                        ex_var_list.append(list(variacion_existe))
                        id.append(item.id)

                    #producto_variacion = [1, 2, 3, 4, 6]
                    #ex_var_list [4, 6, 3, 5]
                    for pr in producto_variacion:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CarroItem.objects.get(id=item_id)
                            item.cantidad += 1
                            item.user = user
                            item.save()
                        else:
                            carro_item = CarroItem.objects.filter(carro=carro)
                            for item in carro_item:
                                item.user = user
                                item.save()
                    
            except:
                pass
            auth.login(request, user)
            messages.success(request,'Inicio de sesion correctamente')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlsparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('mostrar_principal')
        else:
            messages.error(request,'Credenciales invalidas')
            return redirect('inicio-sesion')
    return render(request, 'auth/signin.html')

@login_required
def salir(request):
    logout(request)
    messages.success(request,'Cerraste sesion correctamente')
    return redirect('inicio-sesion')

@login_required
def administracion(request):
    return render(request, 'admin/dashboard.html')

def contrasena_olvidada(request):
    return render(request,'auth/contrasena_olvidada.html')