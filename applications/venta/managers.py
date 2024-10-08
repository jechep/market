# python
from datetime import timedelta
# django
from django.utils import timezone
from django.db import models
#
from applications.producto.models import Producto
from applications.compra.models import Purchase, PurchaseDetail
from django.db.models import Q, Sum, F, FloatField, ExpressionWrapper

class SaleManager(models.Manager):
    """ procedimiento para modelo venta """
    def ventas_no_cerradas(self):
        hoy = timezone.now().date()
        # creamos rango de fecha
        return self.filter(
            date_sale__date=hoy,
            close=False,
            anulado=False
        )
    def total_ventas_dia(self):
        hoy = timezone.now().date()
        consulta = self.filter(
            date_sale__date=hoy,
            close=False,
            anulado=False
        ).aggregate(
            total=Sum('total')
        )
        if consulta['total']:
            return consulta['total']
        else:
            return 0
    def total_ventas_anuladas_dia(self):
        hoy = timezone.now().date()
        consulta = self.filter(
            date_sale__date=hoy,
            close=False,
            anulado=True
        ).aggregate(
            total=Sum('total')
        )
        if consulta['total']:
            return consulta['total']
        else:
            return 0
    def cerrar_ventas(self):
        consulta = self.filter(
            close=False,
        )
        # actualizmos a cerrado
        total = consulta.aggregate(
            total=Sum('amount')
        )['total']
        cerrados = consulta.update(close=True) # devuelve numero de actualizciones

        return cerrados, total
    
    def total_ventas(self):
        return self.filter(
            anulado=False,
        ).aggregate(
            total=Sum('total')
        )['total']
    
    def ventas_en_fechas(self, date_start, date_end):
        return self.filter(
            anulado=False,
            date_sale__range=(date_start, date_end),
        ).order_by('-date_sale')

class SaleDetailManager(models.Manager):
    """ procedimiento modelo product """
    
    def detalle_por_venta(self, id_venta):
        return self.filter(
            sale__id=id_venta
        )

    def ventas_mes_producto(self, id_prod):
        # creamos rango de fecha
        end_date = timezone.now()
        start_date = end_date - timedelta(days=800)
        
        consulta = self.filter(
            sale__anulado=False,
            created__range=(start_date, end_date),
            product__pk=id_prod,
        ).values('sale__date_sale__date', 'product__name').annotate(
            cantidad_vendida=Sum('count'),
        )
        return consulta
    
    def restablecer_stok_num_ventas(self, id_venta):
        prods_en_anulados = []
        for venta_detail in self.filter(sale__id=id_venta):
            #actualizmso producot
            venta_detail.product.count = venta_detail.product.count + venta_detail.count
            venta_detail.product.num_sale = venta_detail.product.num_sale - venta_detail.count
            prods_en_anulados.append(venta_detail.product)
        Producto.objects.bulk_update(prods_en_anulados, ['count', 'num_sale'])
        return True
    
    def resumen_ventas(self):
        return self.filter(
            sale__anulado=False,
            sale__close=True,
        ).values('sale__date_sale__date').annotate(
            total_vendido=Sum(
                F('sale_price')*F('count'),
                output_field=FloatField()
            ),
            total_ganancias=Sum(
                F('sale_price')*F('count') - F('profit')*F('count'),
                output_field=FloatField()
            ),
            num_ventas=Sum('count'),
        )
    
    def resumen_ventas_mes(self):
        #
        return self.filter(
            sale__anulado=False
        ).values('sale__date_sale__date__month', 'sale__date_sale__date__year').annotate(
            cantidad_ventas=Sum('count'),
            total_ventas=Sum(F('sale_price'), output_field=FloatField()),
            ganancia_total=Sum(
                # F('sale_price')*F('count') - F('purchase_price')*F('count'),
                F('profit'),
                output_field=FloatField()
            )
        ).order_by('-sale__date_sale__date__month')
    
    def resumen_ventas_cliente(self, **filters):
        # recibe 3 parametros en un diccionario
        # devuelve lista de ventas en rango de fechas de un cliente
        # y, devuelve el total de ventas en rango de fechas y de cliente

        if filters['date_start'] and filters['date_end'] and filters['cliente']:
            consulta = self.filter(
                anulado=False,
                sale__date_sale__range = (
                    filters['date_start'],
                    filters['date_end'],
                ),
                sale__cliente__pk=filters['cliente'],
            )
            
            lista_ventas = consulta.annotate(
                sub_total=ExpressionWrapper(
                    F('sale_price')*F('count'),
                    output_field=FloatField()
                )
            ).order_by('sale__date_sale')

            total_ventas = consulta.aggregate(
                total_venta=Sum(
                    F('sale_price')*F('count'),
                    output_field=FloatField()
                )
            )['total_venta']

            return lista_ventas, total_ventas
        else:
            return [], 0
        
    # Probando logica para calcular la ganancia por cada producto que se vende
    def verificar_stock(self, producto, cantidad):
        if producto.count <= 0:
            return False, "No se tiene stock para este producto"
        elif producto.count < cantidad:
            return False, f"Solo quedan {producto.count} productos"
        return True, ""

    def obtener_ultima_compra(self, producto):
        return PurchaseDetail.objects.filter(barcode=producto).order_by('-created').first()

    def obtener_dos_ultimas_compras(self, producto):
        return PurchaseDetail.objects.filter(barcode=producto).order_by('-created')[:2]

    def calcular_ganancia(self, carshop_venta):
        car_producto = carshop_venta.product
        cantidad = carshop_venta.count
        sale_price = carshop_venta.sale_price
        almacen_producto = Producto.objects.get(pk=car_producto.id)

        # # Verificar stock
        # stock_disponible, mensaje = self.verificar_stock(producto, cantidad)
        # if not stock_disponible:
        #     return 0, mensaje

        # Obtener la última compra
        ultima_compra = self.obtener_ultima_compra(car_producto)
        if not ultima_compra:
            return 0, "No se encontraron compras para este producto"

        # Comparar stock con la última compra
        if almacen_producto.count <= ultima_compra.count:
            ganancia = sale_price - (ultima_compra.unit_price * cantidad)
            return ganancia, ""

        # Obtener las dos últimas compras
        dos_ultimas_compras = self.obtener_dos_ultimas_compras(car_producto)
        if len(dos_ultimas_compras) < 2:
            return 0, "No se encontraron suficientes compras para este producto"

        ultima_compra, penultima_compra = dos_ultimas_compras
        count_1 = ultima_compra.count
        count_2 = penultima_compra.count
        unit_price_1 = ultima_compra.unit_price
        unit_price_2 = penultima_compra.unit_price
        print('sale_price:', sale_price)
        print('count_1:', count_1)
        print('count_2:', count_2)
        print('unit_price_1:', unit_price_1)
        print('unit_price_2:', unit_price_2)
        print('almacen_producto.count:', almacen_producto.count)

        if almacen_producto.count <= (count_1 + count_2):
            count_2_disponible = almacen_producto.count - count_1
            print('count_2_disponible:', count_2_disponible)
            ganancia = sale_price - (count_2_disponible * unit_price_2) - ((cantidad - count_2_disponible) * unit_price_1)
            print('ganancia:', ganancia)
            return ganancia, ""

        # Calcular el unit_price promedio de todas las compras
        compras = PurchaseDetail.objects.filter(barcode=car_producto)
        total_cantidad = sum(compra.count for compra in compras)
        total_precio = sum(compra.unit_price * compra.count for compra in compras)
        unit_price_promedio = total_precio / total_cantidad

        ganancia = sale_price - (unit_price_promedio * cantidad)
        return ganancia, ""
    # Fin de añadido

class CarShopManager(models.Manager):
    """ procedimiento modelo Carrito de compras """
    def total_cobrar(self):
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
            