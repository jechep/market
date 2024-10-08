from django.urls import path
from . import views

app_name = 'proveedor_app'

urlpatterns = [
    path('proveedor/lista/', views.ProveedorListView.as_view(), name='proveedor_list'),
    path('proveedor/agregar/', views.ProveedorCreateView.as_view(), name='proveedor_add'),
    path('proveedor/editar/<pk>/', views.ProveedorUpdateView.as_view(), name='proveedor_update'),
]