from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Cuenta
# Register your models here.

class CuentaAdmin(UserAdmin):
    list_display = ('email','first_name','last_name', 'username','last_login','date_join','is_active')
    list_display_links = ('email','first_name','last_name')
    readonly_fields = ('last_login', 'date_join')
    ordering = ('-date_join',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Cuenta, CuentaAdmin)