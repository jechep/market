# django
from django import forms
# local
from applications.producto.models import Producto, Categoria, SubCategoria, Marca
from applications.inventario.models import UnidadMedida


class ProveedorForm(forms.ModelForm):
    '''
        Formulario para Producto
        
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
    '''
    nombre = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'Escriba nombre o razón social',
                'class': 'input-group-field',
            }
        )
    )
    numero_documento = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'Número',
                'class': 'input-group-field',
            }
        ),
    )
    tipo_persona = forms.ChoiceField(
        required=True,
        widget=forms.Select(
            attrs = {
                'class': 'input-group-field',
            }
        ),
    )
    tipo_documento = forms.ChoiceField(
        required=True,
        widget=forms.Select(
            attrs = {
                'class': 'input-group-field',
            }
        )
    )
    direccion = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'Escriba aquí',
                'class': 'input-group-field',
            }
        )
    )
    telefono = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs = {
                'placeholder': '(+51)',
                'class': 'input-group-field',
            }
        )
    )
    email = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'example@email.com',
                'class': 'input-group-field',
            }
        )
    )
    contacto = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'Escriba el nombre del contacto',
                'class': 'input-group-field',
            }
        )
    )

    class Meta:
        model = Producto
        fields = (
            'nombre',
            'numero_documento',
            'tipo_persona',
            'tipo_documento',
            'direccion',
            'telefono',
            'email',
            'contacto',
            # 'creado',
            # 'anulado',
            'estado',
        )
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'placeholder': 'Nombre o Razón Social',
                    'class': 'input-group-field',
                    'autocomplete': 'off',
                }
            ),
            'numero_documento': forms.TextInput(
                attrs={
                    'placeholder': 'Número de documento',
                    'class': 'input-group-field',
                    'autocomplete': 'off',
                    'type': 'number',
                }
            ),
            'tipo_persona': forms.Select(
                attrs={
                    'class': 'input-group-field',
                }
            ),
            'tipo_documento': forms.Select(
                attrs={
                    'class': 'input-group-field',
                }
            ),
            'direccion': forms.TextInput(
                attrs={
                    'placeholder': 'Dirección',
                    'class': 'input-group-field',
                    'autocomplete': 'off',
                }
            ),
            'telefono': forms.TextInput(
                attrs={
                    'placeholder': 'Dirección',
                    'class': 'input-group-field',
                    'autocomplete': 'off',
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'placeholder': 'micorreo@ejemplo.com',
                    'class': 'input-group-field',
                    'type': 'email',
                    'autocomplete': 'off',
                }
            ),
            'contacto': forms.TextInput(
                attrs={
                    'placeholder': 'Nombre de Contacto',
                    'class': 'input-group-field',
                    'autocomplete': 'off',
                }
            ),
        }

    #validations
    def clean_numero_documento(self):
        '''
            Valida que el codigo de barras sea unico
        '''
        numero_documento = self.cleaned_data['numero_documento']
        if len(numero_documento) < 11:
            raise forms.ValidationError('Ingrese un número de documento válido')
        return numero_documento

