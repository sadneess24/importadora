from django.urls import path
from .views import (tienda, detalle_producto, buscar, subir_resena, modificar_resena, eliminar_resena)

urlpatterns = [
    path('', tienda, name='tienda'),
    path('categoria/<slug:category_slug>/', tienda, name='productos_por_categoria'),
    path('categoria/<slug:category_slug>/<slug:product_slug>/', detalle_producto, name='detalle_producto'),
    path('buscar/', buscar, name='buscar'),
    path('subir_resena/<int:producto_id>/', subir_resena, name='subir_resena'),
    path('modificar_resena/<int:resena_id>/', modificar_resena, name='modificar_resena'),
    path('eliminar_resena/<int:resena_id>/', eliminar_resena, name='eliminar_resena'),
]