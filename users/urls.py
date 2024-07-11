from django.urls import path  
from .views import registrar, entrar, exit   
urlpatterns = [
    path("registrar/",registrar,name="registrar"),
    path("entrar/",entrar,name="entrar"),
    path("exit/",exit,name="salir"),
]