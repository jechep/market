# Django
from django.db import models
# third-paty
from model_utils.models import TimeStampedModel
# from django.utils.translation import gettext_lazy as _
# local
from .managers import ProductoManager
from applications.inventario.models import UnidadMedida
from applications.proveedor.models import Proveedor # estoy importando el modelo Proveedor de la app proveedor


class Categoria(TimeStampedModel):
    '''
        Categoria del producto
    '''
    nombre = models.CharField('Nombre', max_length=50)
    padre = models.ForeignKey('self', related_name="hijos", on_delete=models.CASCADE, null=True, blank=True)
    estado = models.BooleanField('Estado', default=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nombre
    
    
class SubCategoria(TimeStampedModel):
    '''
        SubCategoria del producto
    '''
    nombre = models.CharField('Nombre', max_length=50)
    categoria = models.ForeignKey(Categoria, related_name="subcategorias", on_delete=models.CASCADE)
    estado = models.BooleanField('Estado', default=True)

    class Meta:
        verbose_name = 'SubCategoria'
        verbose_name_plural = 'SubCategorias'

    def __str__(self):
        return self.nombre
    
    
class Marca(TimeStampedModel):
    '''
        Marca del producto
    '''
    nombre = models.CharField('Nombre', max_length=50)
    codigo = models.CharField('Codigo', max_length=30)
    user = models.ForeignKey('users.User', related_name="marcas", on_delete=models.CASCADE)
    estado = models.BooleanField('Estado', default=True)

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'

    def __str__(self):
        return self.nombre
    
# ==== ESTOY COMENTANDO ESTE MODELO PARA PODER IMPORTAR EL MODELO PROVEEDOR DE LA APP PROVEEDOR ====

# class Proveedor(TimeStampedModel):
#     '''
#         Proveedor
#     '''
#     nombre = models.CharField('Nombre', max_length=70)
#     ruc = models.CharField('RUC', max_length=13)
#     direccion = models.CharField('Direccion', max_length=100)
#     telefono = models.CharField('Telefono', max_length=10)
#     email = models.EmailField('Email', max_length=100)
#     estado = models.BooleanField('Estado', default=True)

#     class Meta:
#         verbose_name = 'Proveedor'
#         verbose_name_plural = 'Proveedores'

#     def __str__(self):
#         return self.nombre
    
    
class Producto(TimeStampedModel):
    '''
        Producto
    '''
    # UNIT_CHOICES = ('0','Kilogramos'),('1','Litros'),('2','Unidades')
    name = models.CharField('Nombre', max_length=50)
    barcode = models.CharField('Codigo de Barras', max_length=13, unique=True)
    category = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategoria, on_delete=models.CASCADE)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    description = models.TextField('Descripcion', max_length=200)
    unit = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE)
    # provider = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    # precio = models.DecimalField('Precio', max_digits=10, decimal_places=2)
    average_cost = models.DecimalField('Costo Promedio', max_digits=7, decimal_places=2, default=0) # average_cost o costo promedio
    purchase_price = models.DecimalField('precio compra', max_digits=7, decimal_places=2) # purchase_price
    sale_price = models.DecimalField('precio venta', max_digits=7, decimal_places=2) # sale_price
    num_sale = models.PositiveIntegerField('numero de ventas', default=0) # num_sale
    num_purchase = models.PositiveIntegerField('numero de compras', default=0) # num_purchase
    count = models.PositiveIntegerField('Stock en Almacen', default=0)
    due_date = models.DateField('Fecha de Vencimiento', blank=True, null=True)
    estado = models.BooleanField('Estado', default=True)
    
    objects = ProductoManager()

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.name