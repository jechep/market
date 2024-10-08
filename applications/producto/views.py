# django
from datetime import datetime
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    View
) 
# local
from applications.venta.models import SaleDetail
from applications.users.mixins import AlmacenPermisoMixin
#
from .models import Producto
from .forms import ProductoForm
from applications.utils import render_to_pdf


class ProductoListView(AlmacenPermisoMixin, ListView):
    template_name = "producto/lista.html"
    context_object_name = 'productos'
    
    def get_queryset(self):
        kword = self.request.GET.get("kword", '')
        order = self.request.GET.get("order", '')
        queryset = Producto.objects.buscar_producto(kword, order)
        return queryset
    
class ProductoCreateView(AlmacenPermisoMixin, CreateView):
    template_name = "producto/form_producto.html"
    form_class = ProductoForm
    success_url = reverse_lazy('producto_app:producto_list')
    
    def form_invalid(self, form):
        # Imprimir los errores del formulario en la consola
        print(form.errors)
        return super().form_invalid(form)
    
class ProductoUpdateView(AlmacenPermisoMixin, UpdateView):
    template_name = "producto/form_producto.html"
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('producto_app:producto_list')
    
class ProductoDeleteView(AlmacenPermisoMixin, DeleteView):
    template_name = "producto/delete.html"
    model = Producto
    success_url = reverse_lazy('producto_app:producto_list')
    
class ProductoDetailView(AlmacenPermisoMixin, DetailView):
    template_name = "producto/detail.html"
    model = Producto
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #
        context['ventas_mes'] = SaleDetail.objects.ventas_mes_producto(self.kwargs['pk'])
        return context
    
class ProductoDetailViewPdf(AlmacenPermisoMixin, View):
    
    def get(self, request, *args, **kwargs):
        producto = Producto.objects.get(id=self.kwargs['pk'])
        data = {
            'producto': producto,
            'ventas_mes': SaleDetail.objects.ventas_mes_producto(self.kwargs['pk'])
        }
        pdf = render_to_pdf('producto/detail-print.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
    
class FiltrosProductoListView(AlmacenPermisoMixin, ListView):
    template_name = "producto/filtros.html"
    context_object_name = 'productos'
    
    def get_queryset(self):
        date_start = self.request.GET.get("date_start", '')
        date_end = self.request.GET.get("date_end", '')

        # Validar formato de fecha
        if date_start:
            try:
                datetime.strptime(date_start, '%Y-%m-%d')
            except ValueError:
                raise ValidationError(f"'{date_start}' no tiene un formato de fecha válido. Debe ser YYYY-MM-DD.")
        
        if date_end:
            try:
                datetime.strptime(date_end, '%Y-%m-%d')
            except ValueError:
                raise ValidationError(f"'{date_end}' no tiene un formato de fecha válido. Debe ser YYYY-MM-DD.")

        # Construir el diccionario de filtros
        filtros = {
            'order': self.request.GET.get("order", ''),
            'kword': self.request.GET.get("kword", ''),
            # 'provider': self.request.GET.get("provider", ''),
            'marca': self.request.GET.get("marca", ''),
        }
        
        if date_start:
            filtros['date_start'] = date_start
        if date_end:
            filtros['date_end'] = date_end

        # Pasar el diccionario de filtros al método filtrar
        queryset = Producto.objects.filtrar(**filtros)
        return queryset