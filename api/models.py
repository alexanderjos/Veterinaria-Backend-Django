from django.db import models
from .choices import Estado, Disponibilidad
import uuid

class Especialidad(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    estado = models.CharField(
        max_length=10,
        choices=Estado.ESTADO_CHOICES,
        default=Estado.ACTIVO,
    )

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    CATEGORIAS = [
        ('medicamento', 'Medicamento'),
        ('vacuna', 'Vacuna'),
        ('higiene', 'Higiene y cuidado'),
        ('alimento', 'Alimento y suplemento'),
        ('venta', 'Producto para venta directa'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    proveedor = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=CATEGORIAS)
    subtipo = models.CharField(max_length=100, blank=True, null=True)
    stock = models.PositiveIntegerField()
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    estado = models.CharField(
        max_length=10,
        choices=Estado.ESTADO_CHOICES,
        default=Estado.ACTIVO,
    )

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class TipoDocumento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=50)
    estado = models.CharField(
        max_length=10,
        choices=Estado.ESTADO_CHOICES,
        default=Estado.ACTIVO,
    )

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Responsable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    documento = models.CharField(max_length=20)
    emergencia = models.CharField(max_length=100, blank=True, null=True)

    # Puedes descomentar esto si ya tienes el modelo TipoDocumento
    # tipodocumento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, related_name='responsables')

    class Meta:
        ordering = ['nombres']

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Mascota(models.Model):
    GENERO_CHOICES = [
        ('Hembra', 'Hembra'),
        ('Macho', 'Macho'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombreMascota = models.CharField(max_length=100)
    especie = models.CharField(max_length=100)
    raza = models.CharField(max_length=100)
    fechaNacimiento = models.DateField()
    genero = models.CharField(max_length=10, choices=GENERO_CHOICES)
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    color = models.CharField(max_length=50)
    observaciones = models.TextField(blank=True, null=True)
    responsable = models.ForeignKey(Responsable, on_delete=models.CASCADE, related_name='mascotas')

    class Meta:
        ordering = ['nombreMascota']

    def __str__(self):
        return self.nombreMascota


class Consultorio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=255)
    disponible = models.CharField(
        max_length=10,
        choices=Disponibilidad.DISPONIBILIDAD_CHOICES,
        default=Disponibilidad.ABIERTO,
    )

    class Meta:
        verbose_name = 'Consultorio'
        verbose_name_plural = 'Consultorios'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} - {self.ubicacion}"
