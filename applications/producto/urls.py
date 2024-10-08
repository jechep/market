from django.urls import path
from . import views

app_name = 'producto_app'

urlpatterns = [
    path('producto/lista/', views.ProductoListView.as_view(), name='producto_list'),
    path('producto/agregar/', views.ProductoCreateView.as_view(), name='producto_add'),
    path('producto/editar/<pk>/', views.ProductoUpdateView.as_view(), name='producto_update'),
    path('producto/eliminar/<pk>/', views.ProductoDeleteView.as_view(), name='producto_delete'),
    path('producto/detalle/<pk>/', views.ProductoDetailView.as_view(), name='producto_detail'),
    path('producto/detalle/print/<pk>/', views.ProductoDetailViewPdf.as_view(), name='producto_print_detail'),
    path('producto/reporte/', views.FiltrosProductoListView.as_view(), name='producto_filtros'),
]