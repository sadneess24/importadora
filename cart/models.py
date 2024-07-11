from django.db import models
from m_tienda.models import *
from m_autentificacion.models import *
# Create your models here.
class Carro(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    
class CarroItem(models.Model):
    user = models.ForeignKey(Cuenta, on_delete=models.CASCADE, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    variaciones = models.ManyToManyField(Variacion, blank=True)
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE, null=True)
    cantidad = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return self.producto.nombre_producto