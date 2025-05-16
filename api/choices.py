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
class Rol:
    RECEPCIONISTA = 'recepcionista'
    VETERINARIO = 'veterinario'
    INVENTARIO = 'inventario'
    ADMINISTRADOR = 'administrador'

    ROL_CHOICES = [
        (RECEPCIONISTA, 'Recepcionista'),
        (VETERINARIO, 'Veterinario'),
        (INVENTARIO, 'Inventario'),
        (ADMINISTRADOR, 'Administrador'),
    ]
