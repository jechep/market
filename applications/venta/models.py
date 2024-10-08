from django.db import models
from django.conf import settings
from django.db.models.signals import pre_delete, post_save
#
from model_utils.models import TimeStampedModel
# from django.utils.translation import gettext_lazy as _

# local apps
from applications.producto.models import Producto
from applications.cliente.models import Cliente

#
from .managers import SaleManager, SaleDetailManager, CarShopManager
from .signals import update_stok_ventas_producto


class Sale(TimeStampedModel):
    """Modelo que representa a una Venta Global"""

    # tipo recibo constantes
    NOTAVENTA = '0'
    BOLETA = '1'
    FACTURA = '2'
    SIN_COMPROBANTE = '3'
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
    TIPO_INVOCE_CHOICES = [
        (NOTAVENTA, 'Nota de Venta'),
        (BOLETA, 'Boleta Electrónica'),
        (FACTURA, 'Factura Electrónica'),
        (SIN_COMPROBANTE, 'Sin Comprobante'),
    ]

    TIPO_PAYMENT_CHOICES = [
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
        (CONTADO, 'Contado'),
        (CREDITO, 'Crédito'),
    ]
    

    cliente = models.ForeignKey(Cliente, related_name="ventas", on_delete=models.CASCADE)
    type_invoce = models.CharField('TIPO', max_length=2, choices=TIPO_INVOCE_CHOICES)
    serie = models.CharField('Serie', max_length=4)
    correlativo = models.CharField('Correlativo', max_length=12)
    type_payment = models.CharField('TIPO PAGO', max_length=2, choices=TIPO_PAYMENT_CHOICES)
    condicion_pago = models.CharField('Estado de Pago', max_length=1, choices=CONDICION_PAGO_CHOICES)
    date_sale = models.DateTimeField('Fecha de Venta',)
    count = models.PositiveIntegerField('Cantidad de Productos')
    subtotal = models.DecimalField('Subtotal', max_digits=10, decimal_places=2)
    igv = models.DecimalField('IGV', max_digits=10, decimal_places=2)
    total = models.DecimalField('Total', max_digits=10, decimal_places=2)
    amount = models.DecimalField('Monto', max_digits=10, decimal_places=2)
    close = models.BooleanField('Venta cerrada', default=False)
    anulado = models.BooleanField('Venta Anulada', default=False,)
    estado = models.BooleanField('Estado', default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='cajero', related_name="user_venta",)

    objects = SaleManager()

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'ventas'

    def __str__(self):
        return 'Nº [' + str(self.id) + '] - ' + str(self.date_sale)



class SaleDetail(TimeStampedModel):
    """Modelo que representa a una venta en detalle"""

    product = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='producto', related_name='product_sale')
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name='Codigo de Venta', related_name='detail_sale')
    count = models.PositiveIntegerField('Cantidad')
    unit_price = models.DecimalField('Valor Unitario', max_digits=10, decimal_places=2)
    sale_price = models.DecimalField('Precio Venta', max_digits=10, decimal_places=2)
    tax = models.DecimalField('Impuesto', max_digits=5, decimal_places=2)
    profit = models.DecimalField('Ganancia', max_digits=7, decimal_places=2, default=0) # ganancia de cada venta
    anulado = models.BooleanField(default=False)
    #

    objects = SaleDetailManager()

    class Meta:
        verbose_name = 'Producto Vendido'
        verbose_name_plural = 'Productos vendidos'

    def __str__(self):
        return str(self.sale.id) + ' - ' + str(self.product.name)
    
    # # Añadido para calcular la ganacia en funcion al promedio de costo del producto
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     self.calculate_profit()

    # def calculate_profit(self):
    #     producto = self.product
    #     self.profit = (self.sale_price - producto.average_cost) * self.count
    #     self.save()
    # # Fin de añadido


class CarShop(TimeStampedModel):
    """Modelo que representa a un carrito de compras"""
    barcode = models.CharField(max_length=13, unique=True)
    product = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='producto', related_name='product_car_venta')
    count = models.PositiveIntegerField('Cantidad')
    unit_price = models.DecimalField('Precio Unitario', max_digits=7, decimal_places=2)
    sale_price = models.DecimalField('Precio Venta', max_digits=7, decimal_places=2)
    
    objects = CarShopManager()

    class Meta:
        verbose_name = 'Carrito de compras'
        verbose_name_plural = 'Carrito de compras'
        ordering = ['-created']

    def __str__(self):
        return str(self.product.name)


# signals for venta
post_save.connect(update_stok_ventas_producto, sender=SaleDetail)
