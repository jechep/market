from django.utils import timezone
from decimal import Decimal, ROUND_HALF_UP
from applications.producto.models import Producto
from .models import Purchase, PurchaseDetail, CarShop

# Redondear a dos decimales
def round_to_two_places(value):
    return Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def procesar_compra(self, **params_compra):
    # recupera la lista de productos en carrito
    productos_en_car = CarShop.objects.all()
    if productos_en_car.count() > 0:            
        # Crear la compra
        compra = Purchase.objects.create(
            proveedor_id=params_compra['proveedor_id'],
            fecha_compra=params_compra['fecha_compra'],
            cantidad=0,
            subtotal=0,
            igv=0,
            total=0,
            tipo_comprobante=params_compra['tipo_comprobante'],
            medio_pago=params_compra['medio_pago'],
            serie=params_compra['serie_comprobante'],
            correlativo=params_compra['numero_comprobante'],
            condicion_pago=params_compra['condicion_pago'],
            user=params_compra['user'],
            # cantidad
            # proveedor
            # condicion_pago
        )
        #
        compras_detalle = []
        productos_en_compra = []
        for producto_car in productos_en_car:
            compra_detalle = PurchaseDetail(
                barcode=producto_car.product, # ¿que producto es?
                compra_cab=compra, # ¿a compra corresponde?
                count=producto_car.count, # ¿cuantos fueron de ese producto?
                purchase_price=producto_car.purchase_price,
                unit_price=producto_car.purchase_price/producto_car.count, # ¿cuanto costo cada uno?
                tax=0.18,
            )
            # actualizmos stok de producto en iteracion
            producto = producto_car.product
            producto.count = producto.count + producto_car.count
            producto.num_purchase = producto.num_purchase + producto_car.count
            #
            compras_detalle.append(compra_detalle)
            productos_en_compra.append(producto)
            #
            compra.cantidad = compra.cantidad + producto_car.count
            compra.subtotal = compra.subtotal + Decimal(producto_car.count*producto_car.unit_price) / Decimal('1.18')
            compra.igv = compra.igv + (Decimal(producto_car.count*producto_car.unit_price) / Decimal('1.18') * Decimal('0.18'))
            compra.total = compra.total + producto_car.count*producto_car.unit_price
            print(compra.total)
        compra.save()
        PurchaseDetail.objects.bulk_create(compras_detalle)
        # actualizamos el stok
        Producto.objects.bulk_update(productos_en_compra, ['count', 'num_purchase'])
        # completada la compra, eliminamos productos delc arrito
        productos_en_car.delete()
        return compra
    else:
        return None
    