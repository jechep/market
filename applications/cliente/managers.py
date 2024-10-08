#python
from datetime import timedelta
#django
from django.db import models
from django.utils import timezone
from django.db.models import Q, F

class ClienteManager(models.Manager):
    '''
        Manager de Cliente - Procedimiento modelo Cliente
    '''
    
    def buscar_cliente(self, kword, order):
        consulta = self.filter(
            Q(name__icontains=kword) |
            Q(numero_documento__icontains=kword)
        )
        # verificamos en que orden se solicita la consulta
        if order == 'date':
            # ordenamos por fecha de creacion
            return consulta.order_by('-created')
        elif order == 'nombre':
            # ordenamos por nombre
            return consulta.order_by('name')
        elif order == 'tipo_persona':
            # ordenamos por cantidad
            return consulta.order_by('count')
        else:
            return consulta.order_by('-created')