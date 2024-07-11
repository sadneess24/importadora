from django.shortcuts import render, redirect
from cart.models import *
from .models import *
from .forms import FormularioOrden
import datetime
import json
from django.http import JsonResponse
# Create your views here.
def pagos(request):
    body = json.loads(request.body)
    orden = Orden.objects.get(user=request.user, is_ordered=False, numero_orden=body['ordenID'])
    pago = Pago(
        user=request.user,
        pago_id=body['transID'],
        metodo_pago=body['metodo_pago'],
        monto_pago=orden.total_orden,
        estado=body['status'],
    )
    pago.save()

    orden.pago = pago
    orden.is_ordered = True
    orden.save()

    carro_items = CarroItem.objects.filter(user=request.user)

    for item in carro_items:
        producto_orden = OrdenProducto()
        producto_orden.orden_id = orden.id
        producto_orden.pago = pago
        producto_orden.user_id = request.user.id
        producto_orden.producto_id = item.producto_id
        producto_orden.cantidad = item.cantidad
        producto_orden.precio_producto = item.producto.precio
        producto_orden.ordenado = True
        producto_orden.save()

        carro_item = CarroItem.objects.get(id=item.id)
        variacion_producto = carro_item.variaciones.all()
        producto_orden.variaciones.set(variacion_producto)
        producto_orden.save()

        producto = Producto.objects.get(id=item.producto_id)
        producto.stock -= item.cantidad
        producto.save()

    CarroItem.objects.filter(user=request.user).delete()

    data = {
        'numero_orden': orden.numero_orden,
        'transID':pago.pago_id,
    }
    return JsonResponse(data)
    #return render(request, 'store/pagos.html')


def realizar_pedido(request, total=0, cantidad=0):
    current_user = request.user
    carro_items = CarroItem.objects.filter(user=current_user)
    contar_carro = carro_items.count()
    if contar_carro <= 0:
        return redirect('tienda')
    
    total_bruto = 0
    impuesto = 0
    for carro_item in carro_items:
        total += (carro_item.producto.precio * carro_item.cantidad)
        cantidad += carro_item.cantidad
    impuesto = (0.19 * total)
    total_bruto = total + impuesto

    if request.method == 'POST':
        form = FormularioOrden(request.POST)
        if form.is_valid():
            data = Orden()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.pais = form.cleaned_data['pais']
            data.region = form.cleaned_data['region']
            data.comuna = form.cleaned_data['comuna']
            data.nota_orden = form.cleaned_data['nota_orden']
            data.total_orden = total_bruto
            data.impuesto = impuesto
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            numero_orden = current_date + str(data.id)
            data.numero_orden = numero_orden
            data.save()

            orden = Orden.objects.get(user=current_user, is_ordered=False, numero_orden=numero_orden)
            contexto = {
                'orden': orden,
                'carro_items': carro_items,
                'impuesto': impuesto,
                'total_bruto': total_bruto,
                'total': total,
            }
            return render(request, 'store/pagos.html', contexto)
    else:
        return redirect('pago')

def orden_completa(request):
    numero_orden = request.GET.get('numero_orden')
    transID = request.GET.get('pago_id')

    try:
        orden = Orden.objects.get(numero_orden=numero_orden, is_ordered=True)
        producto_orden = OrdenProducto.objects.filter(orden_id=orden.id)
        pago = Pago.objects.get(pago_id=transID)

        contexto = {
            'orden': orden,
            'producto_orden': producto_orden,
            'numero_orden': orden.numero_orden,
            'transID': pago.pago_id,
            'pago': pago,
        }
        return render(request,'store/order_complete.html', contexto)
    except (Pago.DoesNotExist, Orden.DoesNotExist):
        return redirect('mostrar_principal')