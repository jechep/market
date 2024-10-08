from django import forms
from .models import Purchase, PurchaseDetail
#

class ComprobanteForm(forms.ModelForm):
    numero_documento = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'input-group-field',
                'placeholder': 'Ingrese RUC o DNI del proveedor',
            }
        )
    )
    nombre_proveedor = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'input-group-field',
                'readonly': 'readonly',
            }
        )
    )
    proveedor_id = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )
    fecha_comprobante = forms.DateField(
        required=True,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'input-group-field',
            }
        )
    )
    tipo_comprobante = forms.ChoiceField(
        required=True,
        choices=Purchase.TIPO_COMPROBANTE_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'input-group-field',
            }
        )
    )
    serie_comprobante = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'input-group-field',
            }
        )
    )
    numero_comprobante = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'input-group-field',
            }
        )
    )
    medio_pago = forms.ChoiceField(
        required=True,
        choices=Purchase.MEDIOS_PAGO_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'input-group-field',
            }
        )
    )

    class Meta:
        model = Purchase
        fields = ['numero_documento', 'nombre_proveedor', 'proveedor_id', 'fecha_comprobante', 'tipo_comprobante', 'serie_comprobante', 'numero_comprobante', 'medio_pago']
        
   
class CompraForm(forms.ModelForm):
    barcode = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'Codigo de barras',
                'class': 'input-group-field',
            }
        )
    )
    count = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(
            attrs = {
                'placeholder': '1',
                'class': 'input-group-field',
            }
        )
    )
    unit_price = forms.DecimalField(
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs = {
                'placeholder': '0.00',
                'class': 'input-group-field',
            }
        )
    )
    purchase_price = forms.DecimalField(
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs = {
                'placeholder': '0.00',
                'class': 'input-group-field',
            }
        )
    )
    # condicion_pago = forms.ChoiceField(
    #     required=False,
    #     choices=Purchase.CONDICION_PAGO_CHOICES,
    #     widget=forms.Select(
    #         attrs = {
    #             'class': 'input-group-field',
    #         }
    #     )
    # )
    
    def clean_count(self):
        count = self.cleaned_data['count']
        if count < 1:
            raise forms.ValidationError('Ingrese una cantidad mayor a cero')
        return count
    
    class Meta:
        model = Purchase
        fields = ['barcode', 'count','unit_price', 'purchase_price']
    
class CompraVoucherForm(forms.Form):

    type_payment = forms.ChoiceField(
        required=False,
        choices=Purchase.CONDICION_PAGO_CHOICES,
        widget=forms.Select(
            attrs = {
                'class': 'input-group-field',
            }
        )
    )
    type_invoice = forms.ChoiceField(
        required=False,
        choices=Purchase.TIPO_COMPROBANTE_CHOICES,
        widget=forms.Select(
            attrs = {
                'class': 'input-group-field',
            }
        )
    )

class CompraDetalleForm(forms.ModelForm):
    class Meta:
        model = PurchaseDetail
        fields = '__all__'