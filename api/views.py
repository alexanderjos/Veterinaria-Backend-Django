from rest_framework import viewsets
from .models import Especialidad
from .serializers import EspecialidadSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Producto
from .serializers import ProductoSerializer
class EspecialidadViewSet(viewsets.ModelViewSet):
    # Definimos el queryset de manera explícita aquí
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer

    # Método que filtra las especialidades activas
    def get_queryset(self):
        # Solo devuelve especialidades cuyo estado sea 'ACTIVO' (insensible a mayúsculas/minúsculas)
        return Especialidad.objects.filter(estado__iexact='activo')

    @action(detail=True, methods=['patch'])
    def desactivar(self, request, pk=None):
        especialidad = self.get_object()
        especialidad.estado = 'INACTIVO'
        especialidad.save()
        return Response({'status': 'especialidad desactivada'})

    # Método para obtener todas las especialidades (activas e inactivas)
    @action(detail=False, methods=['get'], url_path='all')
    def all(self, request):
        # Devuelve todas las especialidades, independientemente de su estado
        especialidades = Especialidad.objects.all()
        serializer = self.get_serializer(especialidades, many=True)
        return Response(serializer.data)



class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    # Filtra productos activos por defecto
    def get_queryset(self):
        return Producto.objects.filter(estado__iexact='activo')

    # Desactiva un producto (cambia su estado a INACTIVO)
    @action(detail=True, methods=['patch'])
    def desactivar(self, request, pk=None):
        producto = self.get_object()
        producto.estado = 'INACTIVO'
        producto.save()
        return Response({'status': 'producto desactivado'})

    # Devuelve todos los productos, sin importar su estado
    @action(detail=False, methods=['get'], url_path='all')
    def all(self, request):
        productos = Producto.objects.all()
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)
