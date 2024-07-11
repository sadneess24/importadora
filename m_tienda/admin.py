from django.contrib import admin
from .models import *
# Register your models here.
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre_producto','precio','stock','categoria','created_date','modified_date','is_available')
    prepopulated_fields = {'slug':('nombre_producto',)}

class VariacionAdmin(admin.ModelAdmin):
    list_display = ('producto','categoria_variacion','valor_variacion','is_active')
    list_editable = ('is_active',)
    list_filter = ('producto','categoria_variacion','valor_variacion')

admin.site.register(Producto, ProductoAdmin)
admin.site.register(Variacion, VariacionAdmin)
admin.site.register(CalificacionResenia)