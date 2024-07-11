from django.urls import path
from .views import (registro, iniciar_sesion, salir, administracion, contrasena_olvidada)

urlpatterns = [
    path('registro/',registro,name='registro'),
    path('inicio-sesion/',iniciar_sesion,name='inicio-sesion'),
    path('salir/',salir,name='salir'),
    path('administracion/',administracion,name='administracion'),
    path('',administracion,name='administracion'),
    path('contraseña_olvidada',contrasena_olvidada,name='contraseña_olvidada'),
]