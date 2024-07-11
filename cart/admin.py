from django.contrib import admin
from .models import *
# Register your models here.

class CarroAdmin(admin.ModelAdmin):
    list_display = ('cart_id','date_added')
    
class CarroItemAdmin(admin.ModelAdmin):
    list_display = ('producto','carro','cantidad','is_active')

admin.site.register(Carro, CarroAdmin)
admin.site.register(CarroItem, CarroItemAdmin)