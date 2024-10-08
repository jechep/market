# django
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import (View, ListView, CreateView, UpdateView, DeleteView)
from django.views.generic.edit import (FormView)
from django.http import JsonResponse
from django.views import View
# local
from applications.producto.models import Producto
from applications.proveedor.models import Proveedor
from applications.utils import render_to_pdf
from applications.users.mixins import ComprasPermisoMixin
#
from .models import Purchase, PurchaseDetail, CarShop
from .forms import CompraForm, CompraDetalleForm, CompraVoucherForm, ComprobanteForm
from .functions import procesar_compra
# from django.views.generic import (View,UpdateView,DeleteView, DeleteView,ListView )


class AddCarPurchaseView(ComprasPermisoMixin, FormView):
    template_name = 'compra/index.html'
    form_class = CompraForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["productos"] = CarShop.objects.all()
        context["total_pagar"] = CarShop.objects.total_pagar()
        context['form_comprobante'] = ComprobanteForm()
        return context
    
    def form_valid(self, form):
        '''Dentro de aqui se pueden recuperar los datos enviados a traves del metodo POST'''
        barcode = form.cleaned_data['barcode']
        count = form.cleaned_data['count']
        unit_price = form.cleaned_data['unit_price']
        purchase_price = form.cleaned_data['purchase_price']
        obj, created = CarShop.objects.get_or_create(
            barcode=barcode,
            defaults={
                'product': Producto.objects.get(barcode=barcode),
                'count': count,
                'unit_price': unit_price,
                'purchase_price': purchase_price,
            }
        )
        #
        if not created:
            obj.count = obj.count + count
            obj.save()
        return super(AddCarPurchaseView, self).form_valid(form)

class CarShopUpdateView(ComprasPermisoMixin, View):
    """ quita en 1 la cantidad en un carshop """

    def post(self, request, *args, **kwargs):
        car = CarShop.objects.get(id=self.kwargs['pk'])
        action = request.POST.get('action')

        if action == 'decrease':
            if car.count > 1:
                car.count -= 1
                car.purchase_price = car.unit_price * car.count
                car.save()
            else:
                car.delete()
        elif action == 'increase':
            car.count += 1
            car.purchase_price = car.unit_price * car.count
            car.save()

        return HttpResponseRedirect(
            reverse(
                'compra_app:compra-index'
            )
        )
        
class CarShopDeleteView(ComprasPermisoMixin, DeleteView):
    model = CarShop
    success_url = reverse_lazy('compra_app:compra-index')

class CarShopDeleteAll(ComprasPermisoMixin, View):
    
    def post(self, request, *args, **kwargs):
        #
        CarShop.objects.all().delete()
        #
        return HttpResponseRedirect(
            reverse(
                'compra_app:compra-index'
            )
        )

class BuscarProveedorView(View):
    def get(self, request, *args, **kwargs):
        numero_documento = request.GET.get('numero_documento', None)
        if numero_documento:
            try:
                proveedor = Proveedor.objects.get(numero_documento=numero_documento)
                data = {
                    'id': proveedor.id,
                    'nombre': proveedor.nombre,
                }
            except Proveedor.DoesNotExist:
                data = {
                    'error': 'Proveedor no encontrado'
                }
        else:
            data = {
                'error': 'Número de documento no proporcionado'
            }
        return JsonResponse(data)

class ProcesoCompraContadoView(ComprasPermisoMixin, View):
    """ Procesa una compra simple """

    def post(self, request, *args, **kwargs):
        form = ComprobanteForm(request.POST)
        if form.is_valid():
            proveedor_id = form.cleaned_data['proveedor_id']
            fecha_comprobante = form.cleaned_data['fecha_comprobante']
            tipo_comprobante = form.cleaned_data['tipo_comprobante']
            serie_comprobante = form.cleaned_data['serie_comprobante']
            numero_comprobante = form.cleaned_data['numero_comprobante']
            medio_pago = form.cleaned_data['medio_pago']
            procesar_compra(
                self=self,
                proveedor_id=proveedor_id,
                fecha_compra=fecha_comprobante,
                tipo_comprobante=tipo_comprobante,
                serie_comprobante=serie_comprobante,
                numero_comprobante=numero_comprobante,
                medio_pago=medio_pago,
                condicion_pago=Purchase.CONTADO,
                user=self.request.user,
            )
            return HttpResponseRedirect(
                reverse(
                    'compra_app:compra-index'
                )
            )
        else:
            return render(request, 'compra/index.html', {'form': form})
                

class CompraVoucherPdf(ComprasPermisoMixin, View):
    
    def get(self, request, *args, **kwargs):
        compra = Purchase.objects.get(id=self.kwargs['pk'])
        data = {
            'compra': compra,
            'detalle_productos': PurchaseDetail.objects.filter(sale__id=self.kwargs['pk'])
        }
        pdf = render_to_pdf('compra/voucher.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

class PurchaseListView(ListView):
    model = Purchase
    template_name = 'compra/compras.html'
    context_object_name = "compras" 
    def get_queryset(self):
        return Purchase.objects.compras_no_cerradas()

class PurchaseDeleteView(DeleteView):
    template_name = 'compra/delete.html'
    model = Purchase
    success_url = reverse_lazy('compra_app:compra-index')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        print("Anulando compra:", self.object.id)  # Mensaje de depuración
        self.object.anulado = True
        self.object.save()
        # actualizmos el stok y compras
        PurchaseDetail.objects.restablecer_stok_num_compras(self.object.id)
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)