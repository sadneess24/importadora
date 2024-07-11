from django.db import models
from django.urls import reverse

# Create your models here.
class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    descripcion = models.TextField(max_length=255, blank=True)
    cat_imagen = models.ImageField(upload_to='images', blank=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def obtener_url(self):
        return reverse('productos_por_categoria', args=[self.slug])

    def __str__(sefl):
        return sefl.nombre_categoria