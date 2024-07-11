from django.urls import path
from .views import (listado, administrar_pagina, administrar_usuarios,editar_usuario,eliminar)

urlpatterns = [
    path('',listado, name='listado'),
    path('administrar_pagina/', administrar_pagina, name='administrar_pagina'),
    path('administrar_usuarios/', administrar_usuarios, name='administrar_usuarios'),
    path('eliminar_usuario/<int:id>/', eliminar, name='eliminar_usuario'),
    path('editar_usuario/<int:id>/', editar_usuario, name='editar_usuario'),
]