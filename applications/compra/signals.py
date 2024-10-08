# disparadores
def update_stok_compras_producto(sender, instance, **kwargs):
    producto = instance.product
    producto.num_purchase = producto.num_purchase + 1
    producto.count = producto.count - instance.count
    producto.save()
    return instance