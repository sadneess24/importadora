from django.db import models
from m_categoria.models import *
from m_autentificacion.models import *

# Create your models here.
class Producto(models.Model):
    nombre_producto = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    descripcion = models.TextField(max_length=500, blank=True)
    precio = models.IntegerField()
    imagen = models.ImageField(upload_to='productos')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def obtener_url(self):
        return reverse('detalle_producto', args=[self.categoria.slug, self.slug])

    def __str__(self):
        return self.nombre_producto
    
class AdministrarVariacion(models.Manager):
    def capacidad(self):
        return super(AdministrarVariacion, self).filter(categoria_variacion='capacidad', is_active=True)
    
    def largo(self):
        return super(AdministrarVariacion, self).filter(categoria_variacion='largo', is_active=True)
    
    def tipo(self):
        return super(AdministrarVariacion, self).filter(categoria_variacion='tipo', is_active=True)
    
    def color(self):
        return super(AdministrarVariacion, self).filter(categoria_variacion='color', is_active=True)

categoria_variacion_choice = (
    ('capacidad','capacidad'),
    ('largo','largo'),
    ('tipo','tipo'),
    ('color','color')
)

class Variacion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    categoria_variacion = models.CharField(max_length=100, choices= categoria_variacion_choice)
    valor_variacion = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = AdministrarVariacion()

    def __str__(self):
        return self.valor_variacion
    

class CalificacionResenia(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    user = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    sujeto = models.CharField(max_length=100, blank=True)
    resenia = models.TextField(max_length=500, blank=True)
    calificacion = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    estado = models.BooleanField(default=True)
    fecha_creado = models.DateTimeField(auto_now_add=True)
    fecha_modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sujeto