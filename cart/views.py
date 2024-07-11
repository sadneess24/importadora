from django.shortcuts import render, redirect, get_object_or_404
from m_tienda.models import *
from cart.models import *
#from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
# Create your views here.
def carrito(request, total=0, cantidad=0, carro_items=None):
    try:
        impuesto = 0
        total_bruto = 0
        if request.user.is_authenticated:
            print("Usuario autenticado:", request.user)
            carro_items = CarroItem.objects.filter(user=request.user, is_active=True)
            print("Carro items para usuario autenticado:", carro_items)
        else:
            carro_id = _cart_id(request)
            print("ID de carrito:", carro_id)
            carro = Carro.objects.get(cart_id=carro_id)
            carro_items = CarroItem.objects.filter(carro=carro, is_active=True)
            print("Carro items para carrito no autenticado:", carro_items)

        for carro_item in carro_items:
            total += (carro_item.producto.precio * carro_item.cantidad)
            cantidad += carro_item.cantidad
        
        impuesto = (0.19 * total)
        total_bruto = total + impuesto

        print(f"Total: {total}, Cantidad: {cantidad}, Items: {carro_items}")
    except ObjectDoesNotExist:
        print("Carro o CarroItem no existen.")
        pass

    contexto = {
        'total': total,
        'cantidad': cantidad,
        'carro_items': carro_items,
        'impuesto': impuesto,
        'total_bruto': total_bruto,
    }
    return render(request, 'store/cart.html', contexto)

def _cart_id(request):
    carro = request.session.session_key
    if not carro:
        request.session.create()
        carro = request.session.session_key
    return carro


def agregar_carrito(request, producto_id):
    current_user = request.user
    producto = Producto.objects.get(id=producto_id)
    if current_user.is_authenticated:
            producto_variacion = []
            if request.method == 'POST':
                for item in request.POST:
                    key = item
                    value = request.POST[key]
                    try:
                        variacion = Variacion.objects.get(producto=producto, categoria_variacion__iexact=key, valor_variacion__iexact=value)
                        producto_variacion.append(variacion)
                    except:
                        pass
            try:
                carro = Carro.objects.get(cart_id=_cart_id(request))
            except Carro.DoesNotExist:
                carro = Carro.objects.create(
                cart_id=_cart_id(request))
            carro.save          

            is_carro_item_exists = CarroItem.objects.filter(producto=producto, user=current_user).exists()
            if is_carro_item_exists:
                carro_item = CarroItem.objects.filter(producto=producto, user=current_user)
                ex_var_list = []
                id = []
                for item in carro_item:
                    variacion_existe = item.variaciones.all()
                    ex_var_list.append(list(variacion_existe))
                    id.append(item.id)

                if producto_variacion in ex_var_list:
                    index = ex_var_list.index(producto_variacion)
                    item_id = id[index]
                    item = CarroItem.objects.get(producto=producto, id=item_id)
                    item.cantidad += 1
                    item.save()
                else:
                    item = CarroItem.objects.create(producto=producto, cantidad=1, user=current_user)
                    if len(producto_variacion) > 0:
                        item.variaciones.clear()
                        item.variaciones.add(*producto_variacion)
                    item.save()
            else:
                carro_item = CarroItem.objects.create(producto=producto, cantidad=1,user=current_user)
                if len(producto_variacion) > 0:
                    carro_item.variaciones.clear()
                    carro_item.variaciones.add(*producto_variacion)
                carro_item.save()
            return redirect('carrito')
            #User
        
    else:
        producto_variacion = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variacion = Variacion.objects.get(producto=producto, categoria_variacion__iexact=key, valor_variacion__iexact=value)
                    producto_variacion.append(variacion)
                except:
                    pass

        try:
            carro = Carro.objects.get(cart_id=_cart_id(request))
        except Carro.DoesNotExist:
            carro = Carro.objects.create(
                cart_id=_cart_id(request)
            )
        carro.save()

        is_carro_item_exists = CarroItem.objects.filter(producto=producto, carro=carro).exists()
        if is_carro_item_exists:
            carro_item = CarroItem.objects.filter(producto=producto, carro=carro)

            ex_var_list = []
            id = []
            for item in carro_item:
                variacion_existe = item.variaciones.all()
                ex_var_list.append(list(variacion_existe))
                id.append(item.id)

            print(ex_var_list)

            if producto_variacion in ex_var_list:
                index = ex_var_list.index(producto_variacion)
                item_id = id[index]
                item = CarroItem.objects.get(producto=producto, id=item_id)
                item.cantidad += 1
                item.save()
            else:
                item = CarroItem.objects.create(producto=producto, cantidad=1, carro=carro)
                if len(producto_variacion) > 0:
                    item.variaciones.clear()
                    item.variaciones.add(*producto_variacion)
                item.save()
        else:
            carro_item = CarroItem.objects.create(producto=producto, cantidad=1,carro=carro)
            if len(producto_variacion) > 0:
                carro_item.variaciones.clear()
                carro_item.variaciones.add(*producto_variacion)
            carro_item.save()
        return redirect('carrito')
    #if request.user.is_authenticated:
        #is_carro_item_exists = CarroItem.objects.filter(producto=producto, user=request.user, is_active=True).exists()
        #if is_carro_item_exists:
            #carro_item = CarroItem.objects.get(producto=producto, user=request.user, is_active=True)
            #carro_item.cantidad += 1
            #carro_item.save()
        #else:
            #carro_item = CarroItem.objects.create(
                #producto=producto,
                #cantidad=1,
                #carro=carro,
                #user=request.user,
            #)
           #if producto_variacion:
               # carro_item.variaciones.add(*producto_variacion)
            #carro_item.save()
    #else:
        #is_carro_item_exists = CarroItem.objects.filter(producto=producto, carro=carro, is_active=True).exists()
        #if is_carro_item_exists:
            #carro_item = CarroItem.objects.get(producto=producto, carro=carro, is_active=True)
            #carro_item.cantidad += 1
            #carro_item.save()
        #else:
            #carro_item = CarroItem.objects.create(
                #producto=producto,
                #cantidad=1,
                #carro=carro,
            #)
            #if producto_variacion:
                #carro_item.variaciones.add(*producto_variacion)
            #carro_item.save()



def eliminar_carro(request, producto_id, carro_item_id):

    producto = get_object_or_404(Producto, id=producto_id)
    try:
        if request.user.is_authenticated:
            carro_item = CarroItem.objects.get(producto=producto, user=request.user, id=carro_item_id)
        else:
            carro = Carro.objects.get(cart_id=_cart_id(request))
            carro_item = CarroItem.objects.get(producto=producto, carro=carro, id=carro_item_id)
        if carro_item.cantidad > 1:
            carro_item.cantidad -= 1
            carro_item.save()
        else:
            carro_item.delete()
    except:
        pass
    return redirect('carrito')

def eliminar_carro_item(request, producto_id, carro_item_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.user.is_authenticated:
        carro_item = CarroItem.objects.get(producto=producto, user=request.user, id=carro_item_id)
    else:
        carro = Carro.objects.get(cart_id=_cart_id(request))
        carro_item = CarroItem.objects.get(producto=producto, carro=carro, id=carro_item_id)
    carro_item.delete()
    return redirect('carrito')

@login_required(login_url='inicio-sesion')
def pago(request, total = 0 , cantidad = 0, carro_items=None):
    try:
        impuesto = 0
        total_bruto = 0
        if request.user.is_authenticated:
            carro_items = CarroItem.objects.filter(user=request.user, is_active=True)
        else:
            carro = Carro.objects.get(cart_id=_cart_id(request))
            carro_items = CarroItem.objects.filter(carro=carro, is_active=True)
        for carro_item in carro_items:
            total +=(carro_item.producto.precio * carro_item.cantidad)
            cantidad += carro_item.cantidad
        impuesto = (0.19*total)
        total_bruto = total + impuesto
    except ObjectDoesNotExist:
        pass
    contexto = {
        'total':total,
        'cantidad':cantidad,
        'carro_items':carro_items,
        'impuesto':impuesto,
        'total_bruto':total_bruto,
    }
    return render(request, 'store/pago.html', contexto)