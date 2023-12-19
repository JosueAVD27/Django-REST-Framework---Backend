from django.db import models

class Producto(models.Model):
    ProductoID = models.BigAutoField(auto_created=True, primary_key=True)
    Nombre = models.CharField(max_length=100)
    Precio = models.DecimalField(max_digits=10, decimal_places=2)
    Stock = models.IntegerField()

class Categoria(models.Model):
    CategoriaID = models.BigAutoField(auto_created=True, primary_key=True)
    Nombre = models.CharField(max_length=50)

class ProductosCategorias(models.Model):
    # Atributos del modelo
    Producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    Categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    class Meta:
        # Declaración de la clase Meta
        unique_together = ('Producto', 'Categoria')  # Puedes usar unique_together para simular una clave primaria compuesta

    def __str__(self):
        return f'{self.producto} - {self.categoria}'

class MovimientosInventario(models.Model):
    MovimientoID = models.BigAutoField(auto_created=True, primary_key=True)
    Producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    Cantidad = models.IntegerField()
    FechaMovimiento = models.DateTimeField()
    TipoMovimiento = models.CharField(max_length=10)
    
    
