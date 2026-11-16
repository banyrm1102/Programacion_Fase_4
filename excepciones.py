
from datetime import datetime


# Excepcion general del sistema
class SoftwareFJError(Exception):
    def __init__(self, mensaje, codigo_error="ERR-GENERIC"):
        super().__init__(mensaje)
        self.codigo_error = codigo_error
        self.timestamp = datetime.now()


# Error en los datos ingresados
class DatoInvalidoError(SoftwareFJError):
    def __init__(self, mensaje):
        super().__init__(mensaje, "ERR-VALIDACION-DATOS")


# Error en los datos de un cliente
class ClienteInvalidoError(DatoInvalidoError):
    pass


# Error cuando un servicio no esta disponible
class ServicioNoDisponibleError(SoftwareFJError):
    def __init__(self, mensaje):
        super().__init__(mensaje, "ERR-SERVICIO-NO-DISPONIBLE")


# Error cuando una reserva no es valida
class ReservaInvalidaError(SoftwareFJError):
    def __init__(self, mensaje):
        super().__init__(mensaje, "ERR-RESERVA-FALLIDA")
