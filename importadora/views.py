from django.shortcuts import render
from m_tienda.models import *

def mostrar_principal(request):
    productos = Producto.objects.all().filter(is_available=True)
    contexto = {
        'productos': productos,
    }
    return render(request,'home/index.html', contexto)
