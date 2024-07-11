from .models import *
from .views import _cart_id

def contadorCarro(request):
    contar_carro = 0
    if 'admin' in request.path:
        return []
    else:
        try:
            carro = Carro.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                carro_items = CarroItem.objects.all().filter(user=request.user)
            carro_items = CarroItem.objects.all().filter(carro=carro[:1])
            for carro_item in carro_items:
                contar_carro += carro_item.cantidad
        except Carro.DoesNotExist:
            contar_carro = 0
    return dict(contar_carro= contar_carro)