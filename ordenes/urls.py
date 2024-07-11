from django.urls import path
from .views import (realizar_pedido,pagos, orden_completa)

urlpatterns = [
    path('realizar_pedido/',realizar_pedido, name='realizar_pedido'),
    path('pagos/',pagos, name='pagos'),
    path('orden-completa/',orden_completa, name='orden-completa')
]
