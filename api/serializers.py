# serializers.py
from rest_framework import serializers
from .models import Especialidad
from .choices import Estado

class EspecialidadSerializer(serializers.ModelSerializer):
    estado = serializers.ChoiceField(choices=Estado.ESTADO_CHOICES, required=False, allow_null=True)

    class Meta:
        model = Especialidad
        fields = ['id', 'nombre', 'estado']
