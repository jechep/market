# django
from django import forms
# local
from .models import Producto, Categoria, SubCategoria, Marca
from applications.inventario.models import UnidadMedida


class ProductoForm(forms.ModelForm):
    '''
        Formulario para Producto
    '''
    category = forms.ModelChoiceField(queryset=Categoria.objects.all(), empty_label="Seleccione una categoría")
    subcategory = forms.ModelChoiceField(queryset=SubCategoria.objects.all(), empty_label="Seleccione una subcategoría")
    marca = forms.ModelChoiceField(queryset=Marca.objects.all(), empty_label="Seleccione una Marca")
    unit = forms.ModelChoiceField(queryset=UnidadMedida.objects.all(), empty_label="Seleccionar...")
    class Meta:
        model = Producto
        fields = (
            'name',
            'barcode',
            'category',
            'subcategory',
            'marca',
            'description',
            'unit',
            # 'provider',
            'purchase_price',
            'sale_price',
            'count',
            'due_date',
            'estado',
        )
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Nombre del producto',
                    'class': 'input-group-field',
                    'autocomplete': 'off',
                }
            ),
            'barcode': forms.TextInput(
                attrs={
                    'placeholder': 'Codigo de barras',
                    'class': 'input-group-field',
                }
            ),
            'category': forms.Select(
                attrs={
                    'class': 'input-group-field',
                }
            ),
            'subcategory': forms.Select(
                attrs={
                    'class': 'input-group-field',
                }
            ),
            'marca': forms.Select(
                attrs={
                    'class': 'input-group-field',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Descripcion del producto',
                    'rows': 3,
                    'class': 'input-group-field',
                }
            ),
            'unit': forms.Select(
                attrs={
                    'class': 'input-group-field',
                }
            ),
            'due_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                }
            ),
            'count': forms.NumberInput(
                attrs={
                    'placeholder': 'Stock del producto',
                    'class': 'input-group-field',
                }
            ),
            'estado': forms.CheckboxInput(
                attrs={
                    'class': 'input-group-field',
                }
            ),
        }
        
    #validations
    def clean_codigo_barras(self):
        '''
            Valida que el codigo de barras sea unico
        '''
        codigo_barras = self.cleaned_data['codigo_barras']
        if len(codigo_barras) < 11:
            raise forms.ValidationError('Ingrese un codigo de barras valido')
        return codigo_barras
    
    def clean_purhcase_price(self):
        '''
            Valida que el precio de compra sea mayor a 0
        '''
        purchase_price = self.cleaned_data['purchase_price']
        if not purchase_price > 0:
            raise forms.ValidationError('Ingrese un precio de compra mayor a cero')
    
    def clean_sale_price(self):
        '''
            Valida que el precio de venta sea mayor a 0
        '''
        sale_price = self.cleaned_data['sale_price']
        purchase_price = self.cleaned_data['purchase_price']
        if not sale_price >= purchase_price:
            raise forms.ValidationError('El precio de venta debe ser mayor o igual al precio de compra')
        return sale_price