from django.urls import path
from .views import ProductosView, CategoriasView, ProductosCategoriasView, MovimientosInventarioView

urlpatterns = [
    path('productos', ProductosView.as_view(), name='productos-list'),
    path('productos/<int:producto_id>', ProductosView.as_view(), name='productos-detail'),
    path('categorias', CategoriasView.as_view(), name='categorias-list'),
    path('categorias/<int:categoria_id>', CategoriasView.as_view(), name='categorias-detail'),
    path('productos_categorias', ProductosCategoriasView.as_view(), name='productos-categorias-list'),
    path('productos_categorias/<int:id>', ProductosCategoriasView.as_view(), name='productos-categorias-detail'),
    path('movimientos_inventario', MovimientosInventarioView.as_view(), name='movimientos-inventario-list'),
    path('movimientos_inventario/<int:movimiento_id>', MovimientosInventarioView.as_view(), name='movimientos-inventario-detail'),
]
