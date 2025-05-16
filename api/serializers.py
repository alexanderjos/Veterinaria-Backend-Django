# serializers.py
from rest_framework import serializers
from .models import *
from .choices import *

class EspecialidadSerializer(serializers.ModelSerializer):
    estado = serializers.ChoiceField(choices=Estado.ESTADO_CHOICES, required=False, default=Estado.ACTIVO)

    class Meta:
        model = Especialidad
        fields = ['id', 'nombre', 'estado']


class ProductoSerializer(serializers.ModelSerializer):
    estado = serializers.ChoiceField(choices=Estado.ESTADO_CHOICES, required=False, default=Estado.ACTIVO)

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'proveedor', 
                  'tipo', 'subtipo','stock','precio_venta','fecha_vencimiento','estado']


class TipoDocumentoSerializer(serializers.ModelSerializer):
    estado = serializers.ChoiceField(choices=Estado.ESTADO_CHOICES, required=False, default=Estado.ACTIVO)

    class Meta:
        model = TipoDocumento
        fields = ['id', 'nombre', 'estado']


class ResponsableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsable
        fields = [
            'id', 'nombres', 'apellidos', 'email', 'telefono',
            'direccion', 'ciudad', 'documento', 'emergencia'
        ]


class MascotaSerializer(serializers.ModelSerializer):
    responsable = ResponsableSerializer()

    class Meta:
        model = Mascota
        fields = [
            'id', 'nombreMascota', 'especie', 'raza', 'fechaNacimiento',
            'genero', 'peso', 'color', 'observaciones', 'responsable'
        ]

    def create(self, validated_data):
        responsable_data = validated_data.pop('responsable')
        responsable = Responsable.objects.create(**responsable_data)
        mascota = Mascota.objects.create(responsable=responsable, **validated_data)
        return mascota

    def update(self, instance, validated_data):
        responsable_data = validated_data.pop('responsable')
        responsable_instance = instance.responsable

        # Actualizar responsable
        for attr, value in responsable_data.items():
            setattr(responsable_instance, attr, value)
        responsable_instance.save()

        # Actualizar mascota
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class ConsultorioSerializer(serializers.ModelSerializer):
    disponible = serializers.ChoiceField(
        choices=Disponibilidad.DISPONIBILIDAD_CHOICES,
        required=False,
        default=Disponibilidad.ABIERTO
    )

    class Meta:
        model = Consultorio
        fields = ['id', 'nombre', 'ubicacion', 'disponible']
