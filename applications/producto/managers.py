#python
from datetime import timedelta
#django
from django.db import models
from django.utils import timezone
from django.db.models import Q, F

class ProductoManager(models.Manager):
    '''
        Manager de Producto - Procedimiento modelo Producto
    '''
    
    def buscar_producto(self, kword, order):
        consulta = self.filter(
            Q(name__icontains=kword) |
            Q(barcode__icontains=kword)
        )
        # verificamos en que orden se solicita la consulta
        if order == 'barcode':
            # ordenamos por fecha de creacion
            return consulta.order_by('barcode')
        elif order == 'date':
            # ordenamos por fecha de creacion
            return consulta.order_by('-created')
        elif order == 'name':
            # ordenamos por nombre
            return consulta.order_by('name')
        elif order == 'count':
            # ordenamos por cantidad
            return consulta.order_by('count')
        else:
            return consulta.order_by('pk')
        
    def update_stock_ventas_producto(self, venta_id):
        #
        consulta = self.filter(product_sale__sale__id=venta_id)
        #
        consulta.update(count=F('count') + 1)
        
    def productos_en_cero(self):
        #
        consulta = self.filter(count__lt=10)
        #
        return consulta
    
    def filtrar(self, **filters):
        filters.setdefault('date_start', '2024-01-01')
        filters.setdefault('date_end', timezone.now().date() + timedelta(1080))
        filters.setdefault('kword', '')
        filters.setdefault('marca', '')
        # filters.setdefault('provider', '')
        filters.setdefault('order', 'created')
        #
        consulta = self.filter(
            due_date__range=(filters['date_start'], filters['date_end'])
        ).filter(
            Q(name__icontains=filters['kword']) | Q(barcode__icontains=filters['kword'])
        ).filter(
            marca__nombre__icontains=filters['marca'],
            # provider__nombre__icontains=filters['provider'],
        )
        
        if filters['order'] == 'name':
            return consulta.order_by('name')
        elif filters['order'] == 'count':
            return consulta.order_by('count')
        elif filters['order'] == 'num':
            return consulta.order_by('-num_sale')
        else:
            return consulta.order_by('-created')
    
    # def activos(self):
    #     return self.filter(estado=True)
    
    # def inactivos(self):
    #     return self.filter(estado=False)
    
    # def search(self, kword):
    #     return self.filter(
    #         Q(nombre__icontains=kword) |
    #         Q(descripcion__icontains=kword)
    #     )
    
    # def categoria(self, categoria):
    #     return self.filter(
    #         categoria=categoria
    #     )
    
    # def subcategoria(self, subcategoria):
    #     return self.filter(
    #         subcategoria=subcategoria
    #     )
    
    # def marca(self, marca):
    #     return self.filter(
    #         marca=marca
    #     )
    
    # def proveedor(self, proveedor):
    #     return self.filter(
    #         proveedor=proveedor
    #     )
    
    # def fecha_vencimiento(self):
    #     return self.filter(
    #         fecha_vencimiento__lt=timezone.now() + timedelta(days=30)
    #     )
    
    # def productos_agotados(self):
    #     return self.filter(
    #         cantidad__lte=0
    #     )
    
    # def productos_stock(self):
    #     return self.filter(
    #         cantidad__gt=0
    #     )
    
    # def productos_menor_stock(self):
    #     return self.filter(
    #         cantidad__lte=F('stock_minimo')
    #     )
    
    # def productos_mayor_stock(self):
    #     return self.filter(
    #         cantidad__gte=F('stock_maximo')
    #     )
    
    # def productos_stock_bajo(self):
    #     return self.filter(
    #         cantidad__lte=F('stock_maximo'),
    #         cantidad__gt=F('stock_minimo')
    #     )
    
    # def productos_stock_medio(self):
    #     return self.filter(
    #         cantidad__lte=F('stock_maximo') * 2,
    #         cantidad__gt=F('stock_maximo')
    #     )
    
    # def productos_stock_alto(self):
    #     return self.filter(
    #         cantidad__gt=F('stock_maximo') * 2
    #     )
    
    # def productos_stock_mayor(self):
    #     return self.filter(
    #         cantidad__gt=F('stock_maximo')
    #     )
    
    # def productos_stock_menor(self):
    #     return self.filter(
    #         cantidad__lt=F('stock_minimo')
    #     )
    
    # def productos_stock_entre(self):
    #     return self.filter(
    #         cantidad__gt=F('stock_minimo'),
    #         cantidad__lt=F('stock_maximo')
    #     )
    
    # def productos_stock_entre_medio(self):
    #     return self