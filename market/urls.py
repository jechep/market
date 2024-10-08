"""
Proyecto de Market
"""
from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('', include('applications.home.urls')),
    # caja app
    re_path('', include('applications.caja.urls')),
    # cliente app
    re_path('', include('applications.cliente.urls')),
    # compra app
    re_path('', include('applications.compra.urls')),
    # inventario app
    # re_path('', include('applications.inventario.urls')),
    # producto app
    re_path('', include('applications.producto.urls')),
    # proveedor app
    re_path('', include('applications.proveedor.urls')),
    # users app
    re_path('', include('applications.users.urls')),
    # venta app
    re_path('', include('applications.venta.urls')),
]
