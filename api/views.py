from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from rest_framework import status
# ViewSet for Especialidad
class EspecialidadViewSet(viewsets.ModelViewSet):
    # Definimos el queryset de manera explícita aquí
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer

    # Método que filtra las especialidades activas
    def get_queryset(self):
        # Solo devuelve especialidades cuyo estado sea 'ACTIVO' (insensible a mayúsculas/minúsculas)
        return Especialidad.objects.all()

    @action(detail=False, methods=['get'], url_path='activos')
    def activos(self, request):
        # Devuelve solo los tipos de documento cuyo estado es 'ACTIVO'
        especialidad_activos = Especialidad.objects.filter(estado__iexact='activo')
        serializer = self.get_serializer(especialidad_activos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def desactivar(self, request, pk=None):
        especialidad = self.get_object()
        especialidad.estado = 'Inactivo'
        especialidad.save()
        return Response({'status': 'especialidad desactivada'})
    # Método para activar una especialidad
    @action(detail=True, methods=['patch'])
    def activar(self, request, pk=None):
        especialidad = self.get_object()
        especialidad.estado = 'Activo'
        especialidad.save()
        return Response({'status': 'especialidad activada'})


    # Método para obtener todas las especialidades (activas e inactivas)
    @action(detail=False, methods=['get'], url_path='all')
    def all(self, request):
        # Devuelve todas las especialidades, independientemente de su estado
        especialidades = Especialidad.objects.all()
        serializer = self.get_serializer(especialidades, many=True)
        return Response(serializer.data)

# ViewSet for Consultorio
class ConsultorioViewSet(viewsets.ModelViewSet):
    queryset = Consultorio.objects.all()  # <- Esto es importante
    serializer_class = ConsultorioSerializer

    def get_queryset(self):
        # Solo consultorios abiertos
        return Consultorio.objects.all()

    @action(detail=False, methods=['get'], url_path='all')
    def all(self, request):
        consultorios = Consultorio.objects.all()
        serializer = self.get_serializer(consultorios, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='cerrar')
    def cerrar(self, request, pk=None):
        consultorio = self.get_object()
        consultorio.disponible = 'Cerrado'
        consultorio.save()
        return Response({'status': 'Consultorio cerrado'})

    @action(detail=True, methods=['patch'], url_path='abrir')
    def abrir(self, request, pk=None):
        consultorio = self.get_object()
        consultorio.disponible = 'Abierto'
        consultorio.save()
        return Response({'status': 'Consultorio abierto'})
    @action(detail=False, methods=['get'], url_path='abiertos')
    def abiertos(self, request):
        # Devuelve solo los tipos de documento cuyo estado es 'ACTIVO'
        especialidad_activos = Especialidad.objects.filter(estado__iexact='abiertos')
        serializer = self.get_serializer(especialidad_activos, many=True)
        return Response(serializer.data)


# ViewSet for TipoDocumento
class TipoDocumentoViewSet(viewsets.ModelViewSet):
    queryset = TipoDocumento.objects.all()
    serializer_class = TipoDocumentoSerializer
    def get_queryset(self):
            # Solo devuelve tipos de documento cuyo estado sea 'ACTIVO'
        return TipoDocumento.objects.all()
    
    @action(detail=False, methods=['get'], url_path='activos')
    def activos(self, request):
        # Devuelve solo los tipos de documento cuyo estado es 'ACTIVO'
        tipos_documento_activos = TipoDocumento.objects.filter(estado__iexact='activo')
        serializer = self.get_serializer(tipos_documento_activos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def desactivar(self, request, pk=None):
        tipo_documento = self.get_object()
        tipo_documento.estado = 'INACTIVO'
        tipo_documento.save()
        return Response({'status': 'Tipo de documento desactivado'})
    # Método para activar un tipo de documento
    @action(detail=True, methods=['patch'])
    def activar(self, request, pk=None):
        tipo_documento = self.get_object()
        tipo_documento.estado = 'Activo'
        tipo_documento.save()
        return Response({'status': 'Tipo de documento activado'})

    @action(detail=False, methods=['get'], url_path='all')
    def all(self, request):
        # Devuelve todos los tipos de documento, independientemente de su estado
        tipos_documento = TipoDocumento.objects.all()
        serializer = self.get_serializer(tipos_documento, many=True)
        return Response(serializer.data)




# ViewSet for Trabajador
class TrabajadorViewSet(viewsets.ModelViewSet):
    queryset = Trabajador.objects.all()
    serializer_class = TrabajadorSerializer
    @action(detail=True, methods=['put'], url_path='reset-password')
    def reset_password(self, request, pk=None):
        trabajador = self.get_object()
        nueva_password = request.data.get('password')

        if not nueva_password or len(nueva_password) < 6:
            return Response({'error': 'La contraseña debe tener al menos 6 caracteres.'}, status=status.HTTP_400_BAD_REQUEST)

        usuario = trabajador.usuario
        usuario.set_password(nueva_password)
        usuario.save()

        return Response({'mensaje': 'Contraseña actualizada correctamente'}, status=status.HTTP_200_OK)
    # Acción personalizada para editar un trabajador
    @action(detail=True, methods=['put'], url_path='editar')
    def edit_trabajador(self, request, pk=None):
        trabajador = self.get_object()  # Obtiene el trabajador por pk
        serializer = TrabajadorSerializer(trabajador, data=request.data, partial=False)  # Deserialize los datos entrantes

        if serializer.is_valid():  # Si los datos del serializador son válidos

            # Aquí controlamos la validación del correo antes de guardar
            usuario_data = serializer.validated_data.get('usuario', None)  # Extraemos los datos del usuario
            if usuario_data and usuario_data.get('email'):  # Verificamos si el correo fue proporcionado
                email = usuario_data['email']

                # Validamos que no exista un usuario con el mismo correo, excluyendo el actual
                if Usuario.objects.filter(email=email).exclude(id=trabajador.usuario.id).exists():
                    return Response({'error': 'El correo electrónico ya está en uso.'}, status=status.HTTP_400_BAD_REQUEST)

            # Si pasa la validación, se guarda
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)  # Respondemos con el trabajador actualizado

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Responde con errores si los datos no son válidos

# ViewSet for Veterinario
class VeterinarioViewSet(viewsets.ModelViewSet):
    queryset = Veterinario.objects.all()
    serializer_class = VeterinarioSerializer

    @action(detail=True, methods=['patch'], url_path='asignar-dias')
    def asignar_dias(self, request, pk=None):
        veterinario = self.get_object()
        dias = request.data.get('dias_trabajo', [])

        if not isinstance(dias, list):
            return Response({'error': 'Se requiere una lista de días.'}, status=status.HTTP_400_BAD_REQUEST)

        # Elimina días anteriores
        DiaTrabajo.objects.filter(veterinario=veterinario).delete()

        # Asigna nuevos días
        for dia in dias:
            DiaTrabajo.objects.create(veterinario=veterinario, dia=dia.upper())

        return Response({'status': 'Días asignados correctamente'})
    #buscar el terabajador por id de trabajador
    @action(detail=False, methods=['get'], url_path='por-trabajador/(?P<trabajador_id>[^/.]+)')
    def por_trabajador(self, request, trabajador_id=None):
        veterinario = get_object_or_404(Veterinario, trabajador__id=trabajador_id)
        serializer = self.get_serializer(veterinario)
        return Response(serializer.data)
    
# ViewSet for Service
class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

    # Filtra servicios activos por defecto
    def get_queryset(self):
        return Servicio.objects.all()

    # Desactiva un servicio (cambia su estado a INACTIVO)
    @action(detail=True, methods=['patch'])
    def desactivar(self, request, pk=None):
        servicio = self.get_object()
        servicio.estado = 'Inactivo'
        servicio.save()
        return Response({'status': 'servicio desactivado'})

    @action(detail=True, methods=['patch'])
    def activar(self, request, pk=None):
        servicio = self.get_object()
        servicio.estado = 'Activo'
        servicio.save()
        return Response({'status': 'servicio activado'})

    # Devuelve todos los servicios, sin importar su estado
    @action(detail=False, methods=['get'], url_path='all')
    def all(self, request):
        servicios = Servicio.objects.all()
        serializer = self.get_serializer(servicios, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='activos')
    def activos(self, request):
        # Devuelve solo los servicios cuyo estado es 'ACTIVO'
        servicios_activos = Servicio.objects.filter(estado__iexact='activo')
        serializer = self.get_serializer(servicios_activos, many=True)
        return Response(serializer.data)














class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    # Filtra productos activos por defecto
    def get_queryset(self):
        return Producto.objects.filter(estado__iexact='Activo')

    # Desactiva un producto (cambia su estado a INACTIVO)
    @action(detail=True, methods=['patch'])
    def desactivar(self, request, pk=None):
        producto = self.get_object()
        producto.estado = 'Inactivo'
        producto.save()
        return Response({'status': 'producto desactivado'})

    # Devuelve todos los productos, sin importar su estado
    @action(detail=False, methods=['get'], url_path='all')
    def all(self, request):
        productos = Producto.objects.all()
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)
class MascotaViewSet(viewsets.ModelViewSet):
    queryset = Mascota.objects.all()
    serializer_class = MascotaSerializer 

    # Filtra mascotas activas por defecto
    @action(detail=False, methods=['get'], url_path='activas')
    def activos(self, request):
        # Devuelve solo las mascotas cuyo estado es 'ACTIVO'
        mascotas_activos = Mascota.objects.filter(estado__iexact='activo')
        serializer = self.get_serializer(mascotas_activos, many=True)
        return Response(serializer.data)
    # Desactiva una mascota (cambia su estado a INACTIVO)
    @action(detail=True, methods=['patch'],url_path='desactivar')
    def desactivar(self, request, pk=None):
        mascota = self.get_object()
        mascota.estado = 'Inactivo'
        mascota.save()
        return Response({'status': 'mascota desactivada'})
    # Método para activar una mascota
    @action(detail=True, methods=['patch'], url_path='activar')
    def activar(self, request, pk=None):
        mascota = self.get_object()
        mascota.estado = 'Activo'
        mascota.save()
        return Response({'status': 'mascota activada'})
    




class ResponsableViewSet(viewsets.ModelViewSet):
    queryset = Responsable.objects.all()
    serializer_class = ResponsableSerializer