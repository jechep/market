from django import forms
from django.utils import timezone
from datetime import datetime
#
from .models import Sale, SaleDetail

class ComprobanteForm(forms.ModelForm):
    numero_documento = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'input-group-field',
                'placeholder': 'Ingrese RUC o DNI del cliente',
            }
        )
    )
    nombre_cliente = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'input-group-field',
                'readonly': 'readonly',
            }
        )
    )
    cliente_id = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )
    date_sale = forms.DateField(
        required=True,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'input-group-field',
            }
        )
    )
    type_invoce = forms.ChoiceField(
        required=True,
        choices=Sale.TIPO_INVOCE_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'input-group-field',
            }
        )
    )
    # serie_comprobante = forms.CharField(
    #     required=True,
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'input-group-field',
    #         }
    #     )
    # )
    # numero_comprobante = forms.CharField(
    #     required=True,
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'input-group-field',
    #         }
    #     )
    # )
    type_payment = forms.ChoiceField(
        required=True,
        choices=Sale.TIPO_PAYMENT_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'input-group-field',
            }
        )
    )
    condicion_pago = forms.ChoiceField(
        required=True,
        choices=Sale.CONDICION_PAGO_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'input-group-field',
            }
        )
    )
    date_payment = forms.DateField(
        required=False,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'input-group-field',
                'readonly': 'readonly',
            }
        )
    )

    class Meta:
        model = Sale
        fields = [
            'numero_documento',
            'nombre_cliente',
            'cliente_id', 
            'date_sale', 
            'type_invoce', 
            # 'serie_comprobante', 
            # 'numero_comprobante', 
            'type_payment',
            'condicion_pago', 
            'date_payment'
        ]
        
    def clean_date_sale(self):
        date_sale = self.cleaned_data['date_sale']
        # Convertir date a datetime
        datetime_sale = datetime.combine(date_sale, datetime.min.time())
        return timezone.make_aware(datetime_sale)

class VentaForm(forms.Form):
    barcode = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'Codigo',
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
                'id': 'count',
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
                'id': 'unit_price',
            }
        )
    )
    sale_price = forms.DecimalField(
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs = {
                'placeholder': '0.00',
                'class': 'input-group-field',
                'id': 'sale_price',
            }
        )
    )
    #
    def clean_count(self):
        count = self.cleaned_data['count']
        if count < 1:
            raise forms.ValidationError('Ingrese una cantidad mayor a cero')
        return count
    

class VentaVoucherForm(forms.Form):

    type_payment = forms.ChoiceField(
        required=False,
        choices=Sale.TIPO_PAYMENT_CHOICES,
        widget=forms.Select(
            attrs = {
                'class': 'input-group-field',
            }
        )
    )
    type_invoce = forms.ChoiceField(
        required=False,
        choices=Sale.TIPO_INVOCE_CHOICES,
        widget=forms.Select(
            attrs = {
                'class': 'input-group-field',
            }
        )
    )