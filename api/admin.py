from django.contrib import admin
from .models import Producto, Categoria, ProductosCategorias, MovimientosInventario

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['ProductoID', 'Nombre', 'Precio', 'Stock']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['CategoriaID', 'Nombre']

@admin.register(ProductosCategorias)
class ProductosCategoriasAdmin(admin.ModelAdmin):
    list_display = ['Producto_id', 'Pategoria_id']

    def Producto_id(self, obj):
        return obj.Producto.ProductoID
    
    def Pategoria_id(self, obj):
        return obj.Categoria.CategoriaID
    
@admin.register(MovimientosInventario)
class MovimientosInventarioAdmin(admin.ModelAdmin):
    list_display = ['MovimientoID','Cantidad', 'FechaMovimiento', 'TipoMovimiento']
    list_filter = ['Producto']
