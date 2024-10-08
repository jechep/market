from django.contrib import admin
#
from .models import Proveedor
    
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'numero_documento','tipo_persona','tipo_documento', 'direccion', 'telefono', 'email', 'estado')
    search_fields = ('nombre', 'numero_documento')

admin.site.register(Proveedor, ProveedorAdmin)