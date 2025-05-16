class Estado:
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    ESTADO_CHOICES = [
        (ACTIVO, 'activo'),
        (INACTIVO, 'inactivo'),
    ]
class Disponibilidad:
    ABIERTO = "abierto"
    CERRADO = "cerrado"
    DISPONIBILIDAD_CHOICES = [
        (ABIERTO, 'Abierto'),
        (CERRADO, 'Cerrado'),
    ]