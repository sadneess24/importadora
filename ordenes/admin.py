from django.contrib import admin
from .models import *
# Register your models here.

class ProductosTabla(admin.TabularInline):
    model = OrdenProducto
    readonly_fields = ('pago','user','producto','cantidad','precio_producto','ordenado')
    extra = 0

class OrdenAdmin(admin.ModelAdmin):
    list_display = ['numero_orden','nombre_completo','phone','email','comuna','total_orden','impuesto','estado','is_ordered','created_at']
    list_filter = ['estado','is_ordered']
    search_fields = ['numero_orden','first_name','last_name','phone','email']
    list_per_page = 20
    inlines = [ProductosTabla]

class PagoAdmin(admin.ModelAdmin):
    list_display = ['user', 'pago_id', 'metodo_pago', 'monto_pago', 'estado', 'creado']
    list_filter = ['metodo_pago', 'estado']
    search_fields = ['pago_id', 'user__username', 'user__email', 'metodo_pago']
    list_per_page = 20

admin.site.register(Pago, PagoAdmin)
admin.site.register(Orden, OrdenAdmin)
admin.site.register(OrdenProducto)