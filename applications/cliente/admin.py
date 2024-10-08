from django.contrib import admin
#
from .models import Cliente
    
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'numero_documento','tipo_persona','tipo_documento', 'direccion', 'telefono', 'email', 'estado')
    search_fields = ('nombre', 'numero_documento')

admin.site.register(Cliente, ClienteAdmin)