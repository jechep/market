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
from applications.users.mixins import ComprasPermisoMixin
#
from .models import Proveedor
from .forms import ProveedorForm


class ProveedorListView(ComprasPermisoMixin, ListView):
    template_name = "proveedor/lista.html"
    context_object_name = 'proveedores'
    
    def get_queryset(self):
        kword = self.request.GET.get("kword", '')
        order = self.request.GET.get("order", '')
        queryset = Proveedor.objects.buscar_proveedor(kword, order)
        return queryset
    
class ProveedorCreateView(ComprasPermisoMixin, CreateView):
    template_name = "proveedor/form_proveedor.html"
    form_class = ProveedorForm
    success_url = reverse_lazy('proveedor_app:proveedor_list')
    
    def form_invalid(self, form):
        # Imprimir los errores del formulario en la consola
        print(form.errors)
        return super().form_invalid(form)
    
class ProveedorUpdateView(ComprasPermisoMixin, UpdateView):
    template_name = "proveedor/form_proveedor.html"
    model = Proveedor
    form_class = ProveedorForm
    success_url = reverse_lazy('proveedor_app:proveedor_list')
    
# class ProductoDeleteView(AlmacenPermisoMixin, DeleteView):
#     template_name = "producto/delete.html"
#     model = Producto
#     success_url = reverse_lazy('producto_app:producto_list')
    

    

    
# class FiltrosProductoListView(AlmacenPermisoMixin, ListView):
#     template_name = "producto/filtros.html"
#     context_object_name = 'productos'
    
#     def get_queryset(self):
#         date_start = self.request.GET.get("date_start", '')
#         date_end = self.request.GET.get("date_end", '')

#         # Validar formato de fecha
#         if date_start:
#             try:
#                 datetime.strptime(date_start, '%Y-%m-%d')
#             except ValueError:
#                 raise ValidationError(f"'{date_start}' no tiene un formato de fecha válido. Debe ser YYYY-MM-DD.")
        
#         if date_end:
#             try:
#                 datetime.strptime(date_end, '%Y-%m-%d')
#             except ValueError:
#                 raise ValidationError(f"'{date_end}' no tiene un formato de fecha válido. Debe ser YYYY-MM-DD.")

#         # Construir el diccionario de filtros
#         filtros = {
#             'kword': self.request.GET.get("kword", ''),
#             'provider': self.request.GET.get("provider", ''),
#             'marca': self.request.GET.get("marca", ''),
#             'order': self.request.GET.get("order", ''),
#         }
        
#         if date_start:
#             filtros['date_start'] = date_start
#         if date_end:
#             filtros['date_end'] = date_end

#         # Pasar el diccionario de filtros al método filtrar
#         queryset = Producto.objects.filtrar(**filtros)
#         return queryset