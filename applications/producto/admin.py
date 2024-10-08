from django.contrib import admin
#
from .models import Categoria, SubCategoria, Producto, Marca


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('name', 'barcode', 'category', 'subcategory', 'marca', 'count', 'purchase_price', 'sale_price', 'due_date', 'estado')
    search_fields = ('name', 'barcode')
    list_filter = ('category', 'subcategory', 'marca', 'due_date', 'estado')
    # list_per_page = 10
    # ordering = ('-created',)
    



admin.site.register(Producto, ProductoAdmin)
#
admin.site.register(Categoria)
#
admin.site.register(SubCategoria)
#
admin.site.register(Marca)