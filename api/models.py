from django.db import models
from .choices import Estado  # Importamos los choices

import uuid

class Especialidad(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    estado = models.CharField(
        max_length=10,
        choices=Estado.ESTADO_CHOICES,
        default=Estado.ACTIVO,
    )

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    proveedor = models.CharField(max_length=100)

    CATEGORIAS = [
        ('medicamento', 'Medicamento'),
        ('vacuna', 'Vacuna'),
        ('higiene', 'Higiene y cuidado'),
        ('alimento', 'Alimento y suplemento'),
        ('venta', 'Producto para venta directa'),
    ]
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

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
class TipoDocumento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre=models.CharField(max_length=50)
    estado = models.CharField(
        max_length=10,
        choices=Estado.ESTADO_CHOICES,
        default=Estado.ACTIVO,
    )
    def __str__(self):
        return f"{self.nombre} "
    class Meta:
        ordering = ['nombre']

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

    #tipodocumento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, related_name='tipodedocumento')


    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
    class Meta:
        ordering = ['nombres']



class Mascota(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombreMascota = models.CharField(max_length=100)
    especie = models.CharField(max_length=100)
    raza = models.CharField(max_length=100)
    fechaNacimiento = models.DateField()
    genero = models.CharField(max_length=10, choices=[('Hembra', 'Hembra'), ('Macho', 'Macho')])
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    color = models.CharField(max_length=50)
    observaciones = models.TextField(blank=True, null=True)
    
    responsable = models.ForeignKey(Responsable, on_delete=models.CASCADE, related_name='mascotas')

    def __str__(self):
        return self.nombreMascota
    class Meta:
        ordering = ['nombreMascota']


# Create your models here.
class Consultorio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=255)
    disponible = models.CharField(
        max_length=10,
        choices=Disponibilidad.DISPONIBILIDAD_CHOICES,
        default='ABIERTO'
    )

    class Meta:
        verbose_name = 'Consultorio'
        verbose_name_plural = 'Consultorios'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.ubicacion}"
# Create your models here.
