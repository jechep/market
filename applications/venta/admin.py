from django.contrib import admin
#
from .models import Sale, SaleDetail


class SaleAdmin(admin.ModelAdmin):
    list_display = (
        'date_sale',
        'count',
        'subtotal',
        'igv',
        'total',
        'amount',
        'user',
        'close',
        'anulado',
    )
    list_filter = ('cliente','serie','correlativo','condicion_pago','type_invoce', 'type_payment', 'anulado', 'user', )


class SaleDetailAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'sale',
        'count',
        'anulado',
    )
    search_fields = ('product__name',)


admin.site.register(Sale, SaleAdmin)
#
admin.site.register(SaleDetail, SaleDetailAdmin)