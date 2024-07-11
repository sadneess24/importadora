from django.db import models
from m_autentificacion.models import *
from m_tienda.models import *

# Create your models here.
class Pago (models.Model):
    user = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    pago_id = models.CharField(max_length=100)
    metodo_pago = models.CharField(max_length=100)
    monto_pago = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    creado = models.DateTimeField(auto_now_add=True)
    
    def _str__(self) :
        return self.pago_id
    

class Orden(models.Model):
    STATUS = (
        ('Nuevo','nuevo'),
        ('Aceptado','aceptado'),
        ('Completado','completado'),
        ('Cancelado','cancelado'),
    )
    
    user = models.ForeignKey(Cuenta, on_delete=models.SET_NULL, null=True)
    pago = models.ForeignKey(Pago, on_delete=models.SET_NULL, null=True)
    numero_orden = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    pais = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    comuna = models.CharField(max_length=50)
    nota_orden = models.CharField(max_length=100, blank=True)
    total_orden = models.FloatField()
    impuesto = models. FloatField()
    estado = models.CharField(max_length=10,choices=STATUS, default='Nuevo')
    ip = models.CharField(blank=True,max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def nombre_completo(self):
        return f'{self.first_name} {self.last_name}'
    
    def direccion_completa(self):
        return f'{self.address_line_1} {self.address_line_2}'

    def __str__(self):
        return self.first_name
    
class OrdenProducto(models.Model) :
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    pago = models.ForeignKey(Pago, on_delete=models.SET_NULL,blank=True, null=True)
    user = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE)
    variaciones = models.ManyToManyField(Variacion, blank=True)
    cantidad = models.IntegerField()
    precio_producto = models.FloatField()
    ordenado = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.producto.nombre_producto