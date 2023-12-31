from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import Producto, Categoria, ProductosCategorias, MovimientosInventario
import json
from datetime import datetime
from django.utils import timezone


@method_decorator(csrf_exempt, name="dispatch")
class ProductosView(View):
    def get(self, request, producto_id=None):
        if producto_id:
            try:
                producto = Producto.objects.get(ProductoID=producto_id)
                data = {
                    "message": "Success",
                    "producto": {
                        "id": producto.ProductoID,
                        "nombre": producto.Nombre,
                        "precio": str(producto.Precio),
                        "stock": producto.Stock,
                    },
                }
            except Producto.DoesNotExist:
                data = {"message": "Producto not found..."}
        else:
            productos = Producto.objects.all().order_by('-ProductoID')
            if productos:
                data = {
                    "message": "Success",
                    "productos": [
                        {
                            "id": p.ProductoID,
                            "nombre": p.Nombre,
                            "precio": str(p.Precio),
                            "stock": p.Stock,
                        }
                        for p in productos
                    ],
                }
            else:
                data = {"message": "Productos not found..."}

        return JsonResponse(data)

    def post(self, request):
        try:
            data = json.loads(request.body)
            producto = Producto.objects.create(
                Nombre=data["nombre"], Precio=data["precio"], Stock=data["stock"]
            )
            data = {
                "message": "Success",
                "producto": {
                    "id": producto.ProductoID,
                    "nombre": producto.Nombre,
                    "precio": str(producto.Precio),
                    "stock": producto.Stock,
                },
            }
        except Exception as e:
            data = {"message": "Error", "error": str(e)}

        return JsonResponse(data)

    def put(self, request, producto_id):
        try:
            data = json.loads(request.body)
            producto = Producto.objects.get(ProductoID=producto_id)
            old_stock = producto.Stock  # Save the old stock for comparison
            producto.Nombre = data['nombre']
            producto.Precio = data['precio']
            producto.Stock = data['stock'] 
            nuevo_stock = data['stock']
            # Verifica si el campo de stock ha sido modificado
            if nuevo_stock != old_stock:
                producto.Stock = nuevo_stock
                producto.save()

                # Calcula la diferencia en el stock
                stock_difference = nuevo_stock - old_stock

                # Crea una entrada de movimiento
                movimiento_tipo = 'Entrada' if stock_difference > 0 else 'Salida'
                movimiento_cantidad = abs(stock_difference)
                fecha_movimiento = datetime.now()

                movimiento = MovimientosInventario.objects.create(
                    Producto=producto,
                    Cantidad=movimiento_cantidad,
                    FechaMovimiento=fecha_movimiento,
                    TipoMovimiento=movimiento_tipo
                )

                data = {
                    'message': 'Success',
                    'producto': {
                        'id': producto.ProductoID,
                        'nombre': producto.Nombre,
                        'precio': str(producto.Precio),
                        'stock': producto.Stock
                    },
                    'movimiento': {
                        'id': movimiento.MovimientoID,
                        'producto_id': movimiento.Producto.ProductoID,
                        'cantidad': movimiento.Cantidad,
                        'fecha_movimiento': movimiento.FechaMovimiento,
                        'tipo_movimiento': movimiento.TipoMovimiento
                    }
                }
            else:
                producto.save()
                # Si no hubo cambios en el stock, solo devuelve la información del producto
                data = {
                    'message': 'Success',
                    'producto': {
                        'id': producto.ProductoID,
                        'nombre': producto.Nombre,
                        'precio': str(producto.Precio),
                        'stock': producto.Stock
                    }
                }
        except Producto.DoesNotExist:
            data = {'message': 'Producto not found...'}
        except Exception as e:
            data = {'message': 'Error', 'error': str(e)}

        return JsonResponse(data)

    def delete(self, request, producto_id):
        try:
            producto = Producto.objects.get(ProductoID=producto_id)
            producto.delete()
            data = {"message": "Success"}
        except Producto.DoesNotExist:
            data = {"message": "Producto not found..."}
        except Exception as e:
            data = {"message": "Error", "error": str(e)}

        return JsonResponse(data)


@method_decorator(csrf_exempt, name="dispatch")
class CategoriasView(View):
    def get(self, request, categoria_id=None):
        if categoria_id:
            try:
                categoria = Categoria.objects.get(CategoriaID=categoria_id)
                data = {
                    "message": "Success",
                    "categoria": {
                        "id": categoria.CategoriaID,
                        "nombre": categoria.Nombre,
                    },
                }
            except Categoria.DoesNotExist:
                data = {"message": "Categoria not found..."}
        else:
            categorias = Categoria.objects.all().order_by('-CategoriaID')
            if categorias:
                data = {
                    "message": "Success",
                    "categorias": [
                        {"id": c.CategoriaID, "nombre": c.Nombre} for c in categorias
                    ],
                }
            else:
                data = {"message": "Categorias not found..."}

        return JsonResponse(data)

    def post(self, request):
        try:
            data = json.loads(request.body)
            categoria = Categoria.objects.create(Nombre=data["nombre"])
            data = {
                "message": "Success",
                "categoria": {"id": categoria.CategoriaID, "nombre": categoria.Nombre},
            }
        except Exception as e:
            data = {"message": "Error", "error": str(e)}

        return JsonResponse(data)

    def put(self, request, categoria_id):
        try:
            data = json.loads(request.body)
            categoria = Categoria.objects.get(CategoriaID=categoria_id)
            categoria.Nombre = data["nombre"]
            categoria.save()
            data = {
                "message": "Success",
                "categoria": {"id": categoria.CategoriaID, "nombre": categoria.Nombre},
            }
        except Categoria.DoesNotExist:
            data = {"message": "Categoria not found..."}
        except Exception as e:
            data = {"message": "Error", "error": str(e)}

        return JsonResponse(data)

    def delete(self, request, categoria_id):
        try:
            categoria = Categoria.objects.get(CategoriaID=categoria_id)
            categoria.delete()
            data = {"message": "Success"}
        except Categoria.DoesNotExist:
            data = {"message": "Categoria not found..."}
        except Exception as e:
            data = {"message": "Error", "error": str(e)}

        return JsonResponse(data)


@method_decorator(csrf_exempt, name="dispatch")
class ProductosCategoriasView(View):
    def get(self, request, producto_id=None, categoria_id=None):
        if producto_id and categoria_id:
            try:
                productos_categorias = ProductosCategorias.objects.select_related(
                    "Producto", "Categoria"
                ).get(id=producto_id, CategoriaID=categoria_id)
                data = {
                    "message": "Success",
                    "productos_categorias": {
                        "id": productos_categorias.id,
                        "producto_id": productos_categorias.Producto.ProductoID,
                        "producto_nombre": productos_categorias.Producto.Nombre,
                        "categoria_id": productos_categorias.Categoria.CategoriaID,
                        "categoria_nombre": productos_categorias.Categoria.Nombre,
                    },
                }
            except ProductosCategorias.DoesNotExist:
                data = {"message": "ProductosCategorias not found..."}
        else:
            productos_categorias = ProductosCategorias.objects.all().order_by("-id")
            
            if productos_categorias:
                data = {
                    "message": "Success",
                    "productos_categorias": [
                        {
                            "id": pc.id,
                            "producto_id": pc.Producto.ProductoID,
                            "producto_nombre": pc.Producto.Nombre,
                            "categoria_id": pc.Categoria.CategoriaID,
                            "categoria_nombre": pc.Categoria.Nombre,
                        }
                        for pc in productos_categorias
                    ],
                }
            else:
                data = {"message": "ProductosCategorias not found..."}

        return JsonResponse(data)

    def post(self, request):
        try:
            data = json.loads(request.body)
            producto_id = data["producto_id"]
            categoria_id = data["categoria_id"]

            producto = Producto.objects.get(ProductoID=producto_id)
            categoria = Categoria.objects.get(CategoriaID=categoria_id)

            productos_categorias = ProductosCategorias.objects.create(
                Producto=producto, Categoria=categoria
            )
            data = {
                "message": "Success",
                "productos_categorias": {
                    "id": productos_categorias.id,
                    "producto_id": productos_categorias.Producto.ProductoID,
                    "categoria_id": productos_categorias.Categoria.CategoriaID,
                },
            }
        except (Producto.DoesNotExist, Categoria.DoesNotExist) as e:
            data = {"message": "Error", "error": str(e)}

        return JsonResponse(data)

    def put(self, request, id):
        try:
            data = json.loads(request.body)
            producto_id = data["producto_id"]
            categoria_id = data["categoria_id"]

            producto = Producto.objects.get(ProductoID=producto_id)
            categoria = Categoria.objects.get(CategoriaID=categoria_id)

            productos_categorias = ProductosCategorias.objects.get(id=id)
            productos_categorias.Producto = producto
            productos_categorias.Categoria = categoria
            productos_categorias.save()

            data = {
                "message": "Success",
                "productos_categorias": {
                    "id": productos_categorias.id,
                    "producto_id": productos_categorias.Producto.ProductoID,
                    "categoria_id": productos_categorias.Categoria.CategoriaID,
                },
            }
        except (
            ProductosCategorias.DoesNotExist,
            Producto.DoesNotExist,
            Categoria.DoesNotExist,
        ) as e:
            data = {"message": "Error", "error": str(e)}

        return JsonResponse(data)

    def delete(self, request, id):
        try:
            productos_categorias = ProductosCategorias.objects.get(id=id)
            productos_categorias.delete()
            data = {"message": "Success"}
        except ProductosCategorias.DoesNotExist:
            data = {"message": "ProductosCategorias not found..."}

        return JsonResponse(data)


@method_decorator(csrf_exempt, name="dispatch")
class MovimientosInventarioView(View):
    def get(self, request, movimiento_id=None):
        if movimiento_id:
            try:
                movimiento = MovimientosInventario.objects.select_related('Producto').get(
                    MovimientoID=movimiento_id
                )
                data = {
                    "message": "Success",
                    "movimiento": {
                        "id": movimiento.MovimientoID,
                        "producto_id": movimiento.Producto.ProductoID,
                        "producto_nombre": movimiento.Producto.Nombre,  # Agregado el nombre del producto
                        "cantidad": movimiento.Cantidad,
                        "fecha_movimiento": movimiento.FechaMovimiento,
                        "tipo_movimiento": movimiento.TipoMovimiento,
                    },
                }
            except MovimientosInventario.DoesNotExist:
                data = {"message": "Movimiento not found..."}
        else:
            movimientos = MovimientosInventario.objects.select_related('Producto').all().order_by("-MovimientoID")
            if movimientos:
                data = {
                    "message": "Success",
                    "movimientos": [
                        {
                            "id": m.MovimientoID,
                            "producto_id": m.Producto.ProductoID,
                            "producto_nombre": m.Producto.Nombre,  # Agregado el nombre del producto
                            "cantidad": m.Cantidad,
                            "fecha_movimiento": m.FechaMovimiento,
                            "tipo_movimiento": m.TipoMovimiento,
                        }
                        for m in movimientos
                    ],
                }
            else:
                data = {"message": "Movimientos not found..."}
                
        return JsonResponse(data)
        
                
    def delete(self, request, movimiento_id):
        try:
            movimiento = MovimientosInventario.objects.get(MovimientoID=movimiento_id)
            movimiento.delete()
            data = {"message": "Success"}
        except MovimientosInventario.DoesNotExist:
            data = {"message": "Movimiento not found..."}
        except Exception as e:
            data = {"message": "Error", "error": str(e)}

        return JsonResponse(data)