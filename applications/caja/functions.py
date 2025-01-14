#
from django.db.models import Prefetch, F, FloatField, ExpressionWrapper
#
from applications.venta.models import Sale, SaleDetail

def detalle_ventas_no_cerradas():
    # recuperamos array de id de las ventas no cerradas
    ventas = Sale.objects.ventas_no_cerradas()
    consulta = ventas.prefetch_related(
        Prefetch(
            'detail_sale',
            queryset=SaleDetail.objects.filter(sale__id__in=ventas).annotate(
                subtotal=ExpressionWrapper(
                    F('sale_price')*F('count'),
                    output_field=FloatField()
                )
            )
        )
    )
    return consulta