# django
from django.urls import path
from . import views

app_name = "compra_app"

urlpatterns = [
    path('buscar-proveedor/', views.BuscarProveedorView.as_view(), name='buscar-proveedor'),
    path('compra/index/', views.AddCarPurchaseView.as_view(), name='compra-index',),
    path('compra/carshop/update/<pk>/', views.CarShopUpdateView.as_view(), name='carshop-update',),
    path('compra/carshop/delete/<pk>/', views.CarShopDeleteView.as_view(), name='carshop-delete',),
    path('compra/carshop/delete-all/', views.CarShopDeleteAll.as_view(), name='carshop-delete_all',),
    path('compra/contado/', views.ProcesoCompraContadoView.as_view(), name='compra-contado',),
    # path('compra/voucher/', views.ProcesoCompraVoucherView.as_view(), name='compra-voucher',),
    # path('compra/voucher-pdf/<pk>/', views.CompraVoucherPdf.as_view(), name='compra-voucher_pdf',),
    path('compra/ultimas-compras/', views.PurchaseListView.as_view(), name='compra-list',),
    path('compra/delete/<pk>/', views.PurchaseDeleteView.as_view(), name='compra-delete',),
]