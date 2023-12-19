from rest_framework import serializers
from .models import Producto, Categoria, ProductosCategorias, MovimientosInventario

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProductosCategoriasSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductosCategorias
        fields = '__all__'

class MovimientosInventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientosInventario
        fields = '__all__'
