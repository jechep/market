# django
# from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import (View, UpdateView, DeleteView, ListView )
from django.views.generic.edit import (FormView)
from django.http import JsonResponse
from django.utils import timezone
# local
from applications.producto.models import Producto
from applications.cliente.models import Cliente
from applications.utils import render_to_pdf
from applications.users.mixins import VentasPermisoMixin
#
from .models import Sale, SaleDetail, CarShop
from .forms import VentaForm, VentaVoucherForm, ComprobanteForm
from .functions import procesar_venta

class AddCarView(VentasPermisoMixin, FormView):
    template_name = 'venta/index.html'
    form_class = VentaForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["productos"] = CarShop.objects.all()
        context["total_cobrar"] = CarShop.objects.total_cobrar()
        # formulario para venta con voucher
        context['form_comprobante'] = ComprobanteForm
        return context
    
    def form_valid(self, form):
        '''
        Dentro de aqui se pueden recuperar los datos enviados
        a traves del metodo POST
        '''
        barcode = form.cleaned_data['barcode']
        count = form.cleaned_data['count']
        unit_price = form.cleaned_data['unit_price']
        sale_price = form.cleaned_data['sale_price']
        product = Producto.objects.get(barcode=barcode)
        
        obj, created = CarShop.objects.get_or_create(
            barcode=barcode,
            defaults={
                'product': product,
                'count': count,
                'unit_price': unit_price,
                'sale_price': sale_price,
            }
        )
        #
        if not created:
            obj.count = obj.count + count
            obj.save()
        return super(AddCarView, self).form_valid(form)
    
class CarShopUpdateView(VentasPermisoMixin, View):
    """ quita en 1 la cantidad en un carshop """
    def post(self, request, *args, **kwargs):
        car = CarShop.objects.get(id=self.kwargs['pk'])
        action = request.POST.get('action')
        
        if action == 'decrease':
            if car.count > 1:
                car.count -= 1
                car.sale_price = car.unit_price * car.count
                car.save()
            else:
                car.delete()
        elif action == 'increase':
            car.count += 1
            car.sale_price = car.unit_price * car.count
            car.save()
        #
        return HttpResponseRedirect(
            reverse(
                'venta_app:venta-index'
            )
        )

class CarShopDeleteView(VentasPermisoMixin, DeleteView):
    model = CarShop
    success_url = reverse_lazy('venta_app:venta-index')

class CarShopDeleteAll(VentasPermisoMixin, View):
    
    def post(self, request, *args, **kwargs):
        #
        CarShop.objects.all().delete()
        #
        return HttpResponseRedirect(
            reverse(
                'venta_app:venta-index'
            )
        )
        
class BuscarClienteView(View):
    def get(self, request, *args, **kwargs):
        numero_documento = request.GET.get('numero_documento', None)
        if numero_documento:
            try:
                cliente = Cliente.objects.get(numero_documento=numero_documento)
                data = {
                    'id': cliente.id,
                    'nombre': cliente.nombre,
                }
            except Cliente.DoesNotExist:
                data = {
                    'error': 'Cliente no encontrado'
                }
        else:
            data = {
                'error': 'Número de documento no proporcionado'
            }
        return JsonResponse(data)

class ProcesoVentaSimpleView(VentasPermisoMixin, View):
    """ Procesa una venta simple """

    def post(self, request, *args, **kwargs):
        #
        procesar_venta(
            self=self,
            type_invoce=Sale.SIN_COMPROBANTE,
            type_payment=Sale.CASH,
            user=self.request.user,
        )
        #
        return HttpResponseRedirect(
            reverse(
                'venta_app:venta-index'
            )
        )

class ProcesoVentaVoucherView(VentasPermisoMixin, FormView):
    def post(self, request, *args, **kwargs):
        form = ComprobanteForm(request.POST)
        if form.is_valid():
            print("Formulario válido. Datos recibidos:")
            cliente_id = form.cleaned_data['cliente_id']
            date_sale = form.cleaned_data['date_sale']
            type_invoce = form.cleaned_data['type_invoce']
            type_payment = form.cleaned_data['type_payment']
            
            venta = procesar_venta(
                self=self,
                cliente_id=cliente_id,
                date_sale=date_sale,
                type_invoce=type_invoce,
                type_payment=type_payment,
                condicion_pago=Sale.CONTADO,
                user=self.request.user,
            )
            if venta:
                print("Venta procesada:", venta.id)
                return HttpResponseRedirect(
                    reverse(
                        'venta_app:venta-voucher_pdf',
                        kwargs={'pk': venta.pk },
                    )
                )
            else:
                print("Error: No se pudo procesar la venta.")
                return HttpResponseRedirect(
                    reverse(
                        'venta_app:venta-index'
                    )
                )
        else:
            print("Formulario inválido. Errores:")
            print(form.errors)
            return HttpResponseRedirect(
                reverse(
                    'venta_app:venta-index'
                )
            )
    
    # Comentado para poder probar otro metodo
    # form_class = ComprobanteForm
    # success_url = '.'
    # template_name = 'venta/voucher_form.html'
    
    # def form_valid(self, form):
    #     proveedor_id = form.cleaned_data['proveedor_id']
    #     date_sale = form.cleaned_data['date_sale']
    #     date_sale = timezone.make_aware(date_sale)
    #     type_payment = form.cleaned_data['type_payment']
    #     type_invoce = form.cleaned_data['type_invoce']
    #     #
    #     venta = procesar_venta(
    #         self=self,
    #         proveedor_id=proveedor_id,
    #         date_sale=date_sale,
    #         serie_comprobante='F001',
    #         numero_comprobante='0001',
    #         type_invoce=type_invoce,
    #         condicion_pago=Sale.CONTADO,
    #         type_payment=type_payment,
    #         user=self.request.user,
    #     )
    #     #
    #     if venta: 
    #         return HttpResponseRedirect(
    #             reverse(
    #                 'venta_app:venta-voucher_pdf',
    #                 kwargs={'pk': venta.pk },
    #             )
    #         )
    #     else:
    #         return HttpResponseRedirect(
    #             reverse(
    #                 'venta_app:venta-index'
    #             )
    #         )
                

class VentaVoucherPdf(VentasPermisoMixin, View):
    
    # def get(self, request, *args, **kwargs):
    #     venta = Sale.objects.get(id=self.kwargs['pk'])
    #     data = {
    #         'venta': venta,
    #         'detalle_productos': SaleDetail.objects.filter(sale__id=self.kwargs['pk'])
    #     }
    #     pdf = render_to_pdf('venta/voucher.html', data)
    #     return HttpResponse(pdf, content_type='application/pdf')
    def get(self, request, *args, **kwargs):
        try:
            print("Iniciando generación de PDF")
            venta = Sale.objects.get(id=self.kwargs['pk'])
            print(f"Venta obtenida: {venta}")
            detalle_productos = SaleDetail.objects.filter(sale__id=self.kwargs['pk'])
            print(f"Detalle de productos: {detalle_productos}")
            
            data = {
                'venta': venta,
                'detalle_productos': detalle_productos
            }
            
            pdf = render_to_pdf('venta/voucher.html', data)
            print("PDF generado correctamente")
            
            return HttpResponse(pdf, content_type='application/pdf')
        except Exception as e:
            print(f"Error al generar el PDF: {e}")
            return HttpResponse("Error al generar el PDF", status=500)


class SaleListView(VentasPermisoMixin, ListView):
    template_name = 'venta/ventas.html'
    context_object_name = "ventas" 
    def get_queryset(self):
        return Sale.objects.ventas_no_cerradas()


class SaleDeleteView(VentasPermisoMixin, DeleteView):
    template_name = "venta/delete.html"
    model = Sale
    success_url = reverse_lazy('venta_app:venta-index')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        print("Anulando venta:", self.object.id)  # Mensaje de depuración
        self.object.anulado = True
        self.object.save()
        # actualizmos sl stok y ventas
        SaleDetail.objects.restablecer_stok_num_ventas(self.object.id)
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)
