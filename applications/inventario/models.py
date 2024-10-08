from django.db import models
# third-paty
from model_utils.models import TimeStampedModel

# Create your models here.
class UnidadMedida(TimeStampedModel):
    '''
        Unidad de Medida
    '''
    nombre = models.CharField('Nombre', max_length=70)
    codigo = models.CharField('Código', max_length=15)
    color = models.CharField('Color', max_length=10)
    accion = models.BooleanField('Estado', default=False)
    estado = models.BooleanField('Estado', default=True)

    class Meta:
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medida'

    def __str__(self):
        return self.nombre