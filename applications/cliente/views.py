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
from .models import Cliente
from .forms import ClienteForm


class ClienteListView(ComprasPermisoMixin, ListView):
    template_name = "cliente/lista.html"
    context_object_name = 'clientes'
    
    def get_queryset(self):
        kword = self.request.GET.get("kword", '')
        order = self.request.GET.get("order", '')
        queryset = Cliente.objects.buscar_cliente(kword, order)
        return queryset
    
class ClienteCreateView(ComprasPermisoMixin, CreateView):
    template_name = "cliente/form_cliente.html"
    form_class = ClienteForm
    success_url = reverse_lazy('cliente_app:cliente_list')
    
    def form_invalid(self, form):
        # Imprimir los errores del formulario en la consola
        print(form.errors)
        return super().form_invalid(form)
    
class ClienteUpdateView(ComprasPermisoMixin, UpdateView):
    template_name = "cliente/form_cliente.html"
    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy('cliente_app:cliente_list')