from django.urls import path
from .views import (carrito, agregar_carrito, eliminar_carro, eliminar_carro_item, pago)
urlpatterns = [
    path('', carrito, name='carrito'),
    path('agregar_carro/<int:producto_id>/', agregar_carrito, name='agregar_carro'),
    path('eliminar_carro/<int:producto_id>/<int:carro_item_id>/', eliminar_carro, name='eliminar_carro'),
    path('eliminar_carro_item/<int:producto_id>/<int:carro_item_id>/', eliminar_carro_item, name='eliminar_carro_item'),
    path('pago/', pago, name='pago'),
]