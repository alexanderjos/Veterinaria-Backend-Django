class Estado:
    ACTIVO = "Activo"
    INACTIVO = "Inactivo"
    ESTADO_CHOICES = [
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
    ]
class Disponibilidad:
    ABIERTO = "Abierto"
    CERRADO = "Cerrado"
    DISPONIBILIDAD_CHOICES = [
        (ABIERTO, 'Abierto'),
        (CERRADO, 'Cerrado'),
    ]