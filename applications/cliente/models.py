# Django
from django.db import models
# third-paty
from model_utils.models import TimeStampedModel
# from django.utils.translation import gettext_lazy as _
# local
from .managers import ClienteManager
    
    
class Cliente(TimeStampedModel):
    '''
        Cliente
    '''
    # tipo persona
    PERSONA_NATURAL = '0'
    PERSONA_JURIDICA = '1'
    # tipo documento
    DNI = '0'
    RUC = '1'
    PASAPORTE = '2'
    CARNET_EXTRANJERIA = '3'
    #
    TIPO_PERSONA_CHOICES = [
        (PERSONA_NATURAL, 'Persona Natural'),
        (PERSONA_JURIDICA, 'Persona Juridica'),
    ]
    #
    TIPO_DOCUMENTO_CHOICES = [
        (DNI, 'DNI'),
        (RUC, 'RUC'),
        (PASAPORTE, 'Pasaporte'),
        (CARNET_EXTRANJERIA, 'Carnet Extranjeria'),
    ]
    
    nombre = models.CharField('Nombre', max_length=100)
    numero_documento = models.CharField('RUC', max_length=13)
    tipo_persona = models.CharField('Tipo Persona', max_length=2, choices=TIPO_PERSONA_CHOICES)
    tipo_documento = models.CharField('Tipo Documento', max_length=2, choices=TIPO_DOCUMENTO_CHOICES)
    direccion = models.CharField('Direccion', max_length=100, null=True, blank=True)
    telefono = models.CharField('Telefono', max_length=10, null=True, blank=True)
    email = models.EmailField('Email', max_length=100, null=True, blank=True)
    fecha_nacimiento = models.DateField('Fecha de Nacimiento', null=True, blank=True)
    contacto = models.CharField('Contacto', max_length=70, null=True, blank=True),
    creado = models.DateTimeField('Fecha de Creacion', auto_now_add=True)
    anulado = models.BooleanField('Estado', default=True)
    estado = models.BooleanField('Estado', default=True)
    
    objects = ClienteManager()

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nombre