# serializers.py
from rest_framework import serializers
from .models import Especialidad
from .choices import Estado
from .models import Producto
class EspecialidadSerializer(serializers.ModelSerializer):
    estado = serializers.ChoiceField(choices=Estado.ESTADO_CHOICES, required=False, allow_null=True)

    class Meta:
        model = Especialidad
        fields = ['id', 'nombre', 'estado']


class ProductoSerializer(serializers.ModelSerializer):
    estado = serializers.ChoiceField(choices=Estado.ESTADO_CHOICES, required=False, allow_null=True)

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'proveedor', 
                  'tipo', 'subtipo','stock','precio_venta','fecha_vencimiento','estado']
        
