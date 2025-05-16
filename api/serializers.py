# serializers.py
from rest_framework import serializers
from .models import *
from .choices import *

class EspecialidadSerializer(serializers.ModelSerializer):
    estado = serializers.ChoiceField(choices=Estado.ESTADO_CHOICES, required=False, default=Estado.ACTIVO)

    class Meta:
        model = Especialidad
        fields = ['id', 'nombre', 'estado']


# Serializador para el modelo TipoDocumento
class TipoDocumentoSerializer(serializers.ModelSerializer):
    estado = serializers.ChoiceField(choices=Estado.ESTADO_CHOICES, required=False, default=Estado.ACTIVO)

    class Meta:
        model = TipoDocumento
        fields = ['id', 'nombre', 'estado']


# Serializador para el modelo Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    rol = serializers.ChoiceField(choices=Rol.ROL_CHOICES, required=False)

    class Meta:
        model = Usuario
        fields = ['id', 'email', 'rol']

    def to_representation(self, instance):
        """ Custom representation to include role name """
        representation = super().to_representation(instance)
        representation['rol'] = instance.get_rol_display()
        return representation


# Serializador para el modelo Trabajador
class TrabajadorSerializer(serializers.ModelSerializer):
    tipodocumento = serializers.PrimaryKeyRelatedField(queryset=TipoDocumento.objects.all())
    usuario = UsuarioSerializer()

    class Meta:
        model = Trabajador
        fields = ['id', 'nombres', 'apellidos', 'email', 'telefono', 'tipodocumento', 'documento', 'usuario']

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario')  # Extraer datos del usuario
        usuario = Usuario.objects.create(**usuario_data)  # Crear usuario
        trabajador = Trabajador.objects.create(usuario=usuario, **validated_data)  # Crear trabajador con el usuario
        return trabajador
class DiaTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaTrabajo
        fields = ['dia']

class VeterinarioSerializer(serializers.ModelSerializer):
    trabajador = serializers.PrimaryKeyRelatedField(queryset=Trabajador.objects.all())
    especialidad = serializers.PrimaryKeyRelatedField(queryset=Especialidad.objects.all())
    dias_trabajo = DiaTrabajoSerializer(many=True, required=False, allow_null=True)  # Usar el serializador anidado

    class Meta:
        model = Veterinario
        fields = ['id', 'trabajador', 'especialidad', 'dias_trabajo']  # Incluir dias_trabajo

    def create(self, validated_data):
        dias_trabajo_data = validated_data.pop('dias_trabajo', [])
        veterinario = Veterinario.objects.create(**validated_data)
        
        # Asociar los días de trabajo si se proporcionaron
        for dia_data in dias_trabajo_data:
            DiaTrabajo.objects.create(veterinario=veterinario, dia=dia_data['dia'])
        
        return veterinario

    def update(self, instance, validated_data):
        dias_trabajo_data = validated_data.pop('dias_trabajo', [])
        
        # Actualiza el veterinario
        instance.trabajador = validated_data.get('trabajador', instance.trabajador)
        instance.especialidad = validated_data.get('especialidad', instance.especialidad)
        instance.save()
        
        # Actualizar los días de trabajo si se proporcionaron (puedes borrarlos y crear nuevos)
        if dias_trabajo_data:
            instance.dias_trabajo.all().delete()
            for dia_data in dias_trabajo_data:
                DiaTrabajo.objects.create(veterinario=instance, dia=dia_data['dia'])
        
        return instance


class TipoDocumentoSerializer(serializers.ModelSerializer):
    estado = serializers.ChoiceField(choices=Estado.ESTADO_CHOICES, required=False, default=Estado.ACTIVO)

    class Meta:
        model = TipoDocumento
        fields = ['id', 'nombre', 'estado']


# Serializador para el modelo Servicio
class ServicioSerializer(serializers.ModelSerializer):
    estado = serializers.ChoiceField(choices=Estado.ESTADO_CHOICES, required=False, default=Estado.ACTIVO)

    class Meta:
        model = Servicio
        fields = ['id', 'nombre', 'precio', 'estado']










class ProductoSerializer(serializers.ModelSerializer):
    estado = serializers.ChoiceField(choices=Estado.ESTADO_CHOICES, required=False, default=Estado.ACTIVO)

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'proveedor', 
                  'tipo', 'subtipo','stock','precio_venta','fecha_vencimiento','estado']


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
