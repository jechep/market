# Django
from django.db import models
# third-paty
from model_utils.models import TimeStampedModel
# from django.utils.translation import gettext_lazy as _
# local
from .managers import ProveedorManager
    
    
class Proveedor(TimeStampedModel):
    '''
        Proveedor
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
    direccion = models.CharField('Direccion', max_length=100)
    telefono = models.CharField('Telefono', max_length=10)
    email = models.EmailField('Email', max_length=100)
    contacto = models.CharField('Contacto', max_length=70)
    creado = models.DateTimeField('Fecha de Creacion', auto_now_add=True)
    anulado = models.BooleanField('Estado', default=True)
    estado = models.BooleanField('Estado', default=True)
    
    objects = ProveedorManager()

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

    def __str__(self):
        return self.id, self.numero_documento, self.nombre
    

'''
# Create your models here.
class Proveedor(TimeStampedModel):
    
    # tipo persona constantes
    PERSONANATURAL = '0'
    PERSONAJURIDICA = '1'
    # tipo documento identidad constantes
    DNI = '1'
    RUC = '2'
    CIP = '3'
    CEE = '4'
    LM = '5'
    PPT = '6'
    #
    TIPO_PERSON_CHOICES = [
        (PERSONANATURAL, 'Persona Natural'),
        (PERSONAJURIDICA, 'Persona Juridica'),
    ]

    TIPO_DOCUMENT_CHOICES = [
        (DNI, 'Documento Nacional de Identidad'),
        (RUC, 'Registro Unico de Contribuyentes'),
        (CIP, 'Carnet de Identidad Policial'),
        (CEE, 'Carnet de Extranjeria'),
        (LM, 'Libreta Militar'),
        (PPT, 'Pasaporte'),
    ]
    
    nombre = models.CharField('Nombre', max_length=200)
    numero_documento = models.CharField('Numero de Documento', max_length=13)
    direccion = models.CharField('Direccion', max_length=100)
    telefono = models.CharField('Telefono', max_length=10)
    email = models.EmailField('Email', max_length=100)
    contacto = models.CharField('Contacto', max_length=100, blank=True, null=True)
    tipo_persona = models.CharField('Tipo de Persona', max_length=1, choices=TIPO_PERSON_CHOICES)
    tipo_documento = models.CharField('Tipo de Documento', max_length=2, choices=TIPO_DOCUMENT_CHOICES)
    anulado = models.BooleanField('Anulado', default=False)
    estado = models.BooleanField('Estado', default=True)

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

    def __str__(self):
        return self.nombre

'''