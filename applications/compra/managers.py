#python
from datetime import timedelta
#django
from django.db import models
from django.utils import timezone
from django.db.models import Q, F, Sum, FloatField, ExpressionWrapper

from applications.producto.models import Producto

class PurchaseManager(models.Manager):
    '''
        Manager de Compra - Procedimiento modelo Compra
    '''
    # proveedor, tipo_documento, serie, correlativo, forma_pago, estado_pago, fecha_compra, subtotal, igv, total, estado
        
    def compras_no_cerradas(self):
        # creamos rango de fecha
        return self.filter(
            estado=True,
            anulado=False
        )
    def total_compras_dia(self):
        consulta = self.filter(
            close=False,
            anulate=False
        ).aggregate(
            total=Sum('amount')
        )
        if consulta['total']:
            return consulta['total']
        else:
            return 0
    def total_compras_anuladas_dia(self):
        consulta = self.filter(
            close=False,
            anulate=True
        ).aggregate(
            total=Sum('amount')
        )
        if consulta['total']:
            return consulta['total']
        else:
            return 0
    def cerrar_compras(self):
        consulta = self.filter(
            close=False,
        )
        # actualizmos a cerrado
        total = consulta.aggregate(
            total=Sum('amount')
        )['total']
        cerrados = consulta.update(close=True) # devuelve numero de actualizciones

        return cerrados, total
    
    def total_compras(self):
        return self.filter(
            anulate=False,
        ).aggregate(
            total=Sum('amount')
        )['total']
    
    def compras_en_fechas(self, date_start, date_end):
        return self.filter(
            anulate=False,
            date_purchase__range=(date_start, date_end),
        ).order_by('-date_purchase')
        
        
        
class PurchaseDetailManager(models.Manager):
    """ procedimiento modelo product """
    
    def detalle_por_compra(self, id_compra):
        return self.filter(
            purchase__id=id_compra
        )

    def compras_mes_producto(self, id_prod):
        # creamos rango de fecha
        end_date = timezone.now()
        start_date = end_date - timedelta(days=800)
        
        consulta = self.filter(
            purchase__anulate=False,
            created__range=(start_date, end_date),
            product__pk=id_prod,
        ).values('purchase__date_purchase__date', 'product__name').annotate(
            cantidad_comprada=Sum('count'),
        )
        return consulta
    
    def restablecer_stok_num_compras(self, id_compra):
        prods_en_anulados = []
        for compra_detail in self.filter(compra_cab__id=id_compra):
            # Actualizamos producto
            compra_detail.barcode.count = compra_detail.barcode.count - compra_detail.count
            compra_detail.barcode.num_purchase = compra_detail.barcode.num_purchase - compra_detail.count
            prods_en_anulados.append(compra_detail.barcode)
        Producto.objects.bulk_update(prods_en_anulados, ['count', 'num_purchase'])
        return True
    
    def resumen_compras(self):
        return self.filter(
            purchase__anulate=False,
            purchase__close=True,
        ).values('purchase__date_purchase__date').annotate(
            total_comprado=Sum(
                F('purchase_price')*F('count'),
                output_field=FloatField()
            ),
            total_ganancias=Sum(
                F('purchase_price')*F('count') - F('purchase_price')*F('count'),
                output_field=FloatField()
            ),
            num_compras=Sum('count'),
        )
    
    def resumen_compras_mes(self):
        #
        return self.filter(
            purchase__anulate=False
        ).values('purchase__date_purchase__date__month', 'purchase__date_purchase__date__year').annotate(
            cantidad_compras=Sum('count'),
            total_compras=Sum(F('purchase_price')*F('count'), output_field=FloatField()),
            ganancia_total=Sum(
                F('purchase_price')*F('count') - F('purchase_price')*F('count'),
                output_field=FloatField()
            )
        ).order_by('-purchase__date_purchase__date__month')
    
    def resumen_compras_proveedor(self, **filters):
        # recibe 3 parametros en un diccionario
        # devuelve lista de ventas en rango de fechas de un proveedor
        # y, devuelve el total de ventas en rango de fechas y de proveedor

        if filters['date_start'] and filters['date_end'] and filters['provider']:
            consulta = self.filter(
                anulate=False,
                purchase__date_purchase__range = (
                    filters['date_start'],
                    filters['date_end'],
                ),
                product__provider__pk=filters['provider'],
            )
            lista_compras = consulta.annotate(
                sub_total=ExpressionWrapper(
                    # considerar que aqui puede usarse product_cost en vez de purchase_price
                    F('purchase_price')*F('count'),
                    output_field=FloatField()
                )
            ).order_by('purchase__date_purchase')

            total_compras = consulta.aggregate(
                total_compra=Sum(
                    # considerar que aqui puede usarse product_cost en vez de purchase_price
                    F('purchase_price')*F('count'),
                    output_field=FloatField()
                )
            )['total_compra']

            return lista_compras, total_compras
        else:
            return [], 0
        
class CarShopManager(models.Manager):
    """ procedimiento modelo Carrito de compras """
    def total_pagar(self):
        consulta = self.aggregate(
            total=Sum(
                F('count')*F('unit_price'),
                output_field=FloatField()
            ),
        )
        if consulta['total']:
            return consulta['total']
        else:
            return 0