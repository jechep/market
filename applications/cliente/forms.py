# django
from django import forms
# local
from applications.producto.models import Producto, Categoria, SubCategoria, Marca
from applications.inventario.models import UnidadMedida


class ClienteForm(forms.ModelForm):
    '''
        Formulario para Clientes
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

