from django.db import models
from django.conf import settings
# third-paty
from model_utils.models import TimeStampedModel
from applications.producto.models import Producto
from applications.proveedor.models import Proveedor
from django.db.models.signals import pre_delete, post_save
# local
from .managers import PurchaseManager, PurchaseDetailManager, CarShopManager
from .signals import update_stok_compras_producto

    

class Purchase(TimeStampedModel):
    '''
        Cabecera de la Compra
    '''
    # tipo recibo constantes
    SIN_COMPROBANTE = '00'
    FACTURA = '01'
    BOLETA = '03'
    NOTACREDITO = '07'
    NOTADEBITO = '08'
    # tipo pago constantes
    EFECTIVO = '1'
    VISA = '2'
    MASTERCARD = '3'
    AMERICANEXPRESS = '4'
    DINERSCLUB = '5'
    CHEQUE = '6'
    TRANSFERENCIA = '7'
    YAPE = '8'
    NIUBIZ = '9'
    IZIPAY = '10'
    VENDEMAS = '11'
    PLIN = '12'
    # condicion de pago constantes
    CONTADO = '1'
    CREDITO = '2'
    #
    TIPO_COMPROBANTE_CHOICES = [
        (SIN_COMPROBANTE, 'Sin Comprobante'),
        (FACTURA, 'Factura'),
        (BOLETA, 'Boleta'),
        (NOTACREDITO, 'Nota de Credito'),
        (NOTADEBITO, 'Nota de Debito'),
    ]
    MEDIOS_PAGO_CHOICES = [
        (EFECTIVO, 'Efectivo'),
        (VISA, 'VISA'),
        (MASTERCARD, 'MasterCard'),
        (AMERICANEXPRESS, 'American Express'),
        (DINERSCLUB, 'Diners Club'),
        (CHEQUE, 'Cheque'),
        (TRANSFERENCIA, 'Depósito o Transferencia'),
        (YAPE, 'Yape'),
        (NIUBIZ, 'Niubiz'),
        (IZIPAY, 'Izipay'),
        (VENDEMAS, 'Vendemas'),
        (PLIN, 'Plin'),
    ]
    CONDICION_PAGO_CHOICES = [
        (CONTADO, 'CONTADO'),
        (CREDITO, 'CREDITO'),
    ]
    
    proveedor = models.ForeignKey(Proveedor, related_name="compras", on_delete=models.CASCADE)
    tipo_comprobante = models.CharField('Tipo de Documento', max_length=2, choices=TIPO_COMPROBANTE_CHOICES)
    serie = models.CharField('Serie', max_length=4)
    correlativo = models.CharField('Correlativo', max_length=12)
    medio_pago = models.CharField('Forma de Pago', max_length=2, choices=MEDIOS_PAGO_CHOICES)
    condicion_pago = models.CharField('Estado de Pago', max_length=1, choices=CONDICION_PAGO_CHOICES)
    fecha_compra = models.DateField('Fecha de Compra')
    cantidad = models.PositiveIntegerField('Cantidad de Productos')
    subtotal = models.DecimalField('Subtotal', max_digits=10, decimal_places=2)
    igv = models.DecimalField('IGV', max_digits=10, decimal_places=2)
    total = models.DecimalField('Total', max_digits=10, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='cajero', related_name="user_compra",)
    anulado = models.BooleanField('Anulado', default=False)
    estado = models.BooleanField('Estado', default=True)
    # proveedor, tipo_documento, serie, correlativo, forma_pago, estado_pago, fecha_compra, subtotal, igv, total, anulado, estado
    
    objects = PurchaseManager()

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'

    def __str__(self):
        return f'Compra {self.id} - {self.proveedor} - {self.tipo_comprobante} - {self.serie}-{self.correlativo}'
    
class PurchaseDetail(TimeStampedModel):
    ''' Detalle de la Compra '''
    compra_cab = models.ForeignKey(Purchase, related_name="detalles", on_delete=models.CASCADE)
    barcode = models.ForeignKey(Producto, related_name="compras", on_delete=models.CASCADE)
    count = models.PositiveIntegerField('Cantidad')
    unit_price = models.DecimalField('Precio Unitario', max_digits=7, decimal_places=2)
    purchase_price = models.DecimalField('Precio', max_digits=7, decimal_places=2)
    tax = models.DecimalField('Impuesto', max_digits=5, decimal_places=2)
    
    objects = PurchaseDetailManager()

    class Meta:
        verbose_name = 'Compra Detalle'
        verbose_name_plural = 'Compras Detalles'

    def __str__(self):
        return self.barcode.nombre
    
    # Añadido para actualizar el promedio de costo del producto
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_product_average_cost()

    def update_product_average_cost(self):
        producto = self.product
        total_quantity = producto.count + self.count
        total_cost = (producto.average_cost * producto.count) + (self.purchase_price * self.count)
        producto.average_cost = total_cost / total_quantity
        producto.save()
    # Fin de añadido
    

class CarShop(TimeStampedModel):
    """ Modelo que representa a un carrito de compras """
    barcode = models.CharField(max_length=13, unique=True)
    product = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='producto', related_name='product_car_compra')
    count = models.PositiveIntegerField('Cantidad')
    unit_price = models.DecimalField('Precio Unitario', max_digits=7, decimal_places=2)
    purchase_price = models.DecimalField('Costo', max_digits=7, decimal_places=2)
    
    objects = CarShopManager()

    class Meta:
        verbose_name = 'Carrito de compras'
        verbose_name_plural = 'Carrito de compras'
        ordering = ['-created']

    def __str__(self):
        return str(self.product.name)


# signals for venta
post_save.connect(update_stok_compras_producto, sender=PurchaseDetail)