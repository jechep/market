from django.urls import path
from . import views

app_name = 'cliente_app'

urlpatterns = [
    path('cliente/lista/', views.ClienteListView.as_view(), name='cliente_list'),
    path('cliente/agregar/', views.ClienteCreateView.as_view(), name='cliente_add'),
    path('cliente/editar/<pk>/', views.ClienteUpdateView.as_view(), name='cliente_update'),
]