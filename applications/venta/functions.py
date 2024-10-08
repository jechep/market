from django.utils import timezone
from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Prefetch
from applications.producto.models import Producto
from .models import Sale, SaleDetail, CarShop

def procesar_venta(self, **params_venta):
    try:
        # recupera la lista de productos en carrito
        productos_en_car = CarShop.objects.all()
        print("Productos en carrito:", productos_en_car)
        if productos_en_car.count() > 0:
            # Verificar si hay suficiente stock para cada producto
            for producto_car in productos_en_car:
                if producto_car.product.count < producto_car.count:
                    print(f"No hay suficiente stock para el producto {producto_car.product.name}")
                    return None  # No hay suficiente stock para algún producto
                
            # crea el objeto venta
            venta = Sale.objects.create(
                cliente_id=params_venta['cliente_id'],
                type_invoce=params_venta['type_invoce'],
                serie='P001',
                correlativo='00000001',
                type_payment=params_venta['type_payment'],
                condicion_pago=params_venta['condicion_pago'],
                date_sale=params_venta['date_sale'],
                count=0,
                subtotal=0,
                igv=0,
                total=0,
                amount=0,
                close = False,
                user=params_venta['user'],
            )
            print("Venta creada:", venta)
            #
            ventas_detalle = []
            productos_en_venta = []
            for producto_car in productos_en_car:
                print("Producto: ", producto_car.product)
                print("Cantidad: ", producto_car.count)
                print("Precio: ", producto_car.sale_price)
                
                # Crear el detalle de la venta
                venta_detalle = SaleDetail(
                    product=producto_car.product, # ¿que producto es?
                    sale=venta, # ¿a cual venta corresponde?
                    count=producto_car.count, # ¿cuantos fueron de ese producto?
                    sale_price=producto_car.sale_price,
                    unit_price=producto_car.sale_price/producto_car.count, # ¿cuanto costo cada uno?
                    profit=0,
                    tax=0.18,
                )
                
                # Calcular la ganancia para cada detalle de venta sin actualizar el stock
                ganancia, mensaje = SaleDetail.objects.calcular_ganancia(producto_car)
                if mensaje:
                    print(f"Error al calcular la ganancia: {mensaje}")
                    raise ValueError(mensaje)
                venta_detalle.profit = ganancia
                venta_detalle.save()
                print("Detalle de venta guardado:", venta_detalle)
                
                # actualizmos stok de producto en iteracion
                producto = producto_car.product
                # producto.count -= producto_car.count
                # print("Nuevo stock:", producto.count)
                producto.num_sale += producto_car.count - 1
                print("Cantidad vendida:", producto.num_sale)
                #
                ventas_detalle.append(venta_detalle)
                productos_en_venta.append(producto)
                
                # Actualizar los valores de la venta
                venta.count = venta.count + producto_car.count
                venta.subtotal = venta.subtotal + Decimal(producto_car.count*producto_car.unit_price) / Decimal('1.18')
                venta.igv = venta.igv + (Decimal(producto_car.count*producto_car.unit_price) / Decimal('1.18') * Decimal('0.18'))
                venta.total = venta.total + producto_car.count*producto_car.unit_price
            
            venta.close = False
            venta.save()
            print("Venta actualizada:", venta)
            
            # Actualizar el stock de los productos
            Producto.objects.bulk_update(productos_en_venta, ['count', 'num_sale'])
            print("Stock de productos actualizado")
            
            # Eliminar productos del carrito
            productos_en_car.delete()
            print("Productos eliminados del carrito")
            
            return venta
        else:
            print("No hay productos en el carrito")
            return None
    except Exception as e:
        print(f"Error al procesar la venta: {e}")
        return None