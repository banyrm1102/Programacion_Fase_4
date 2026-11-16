
from Cliente import Cliente
from servicios import Servicios
from excepciones import ReservaInvalidaError


class Reserva:
    # Constructor de la reserva
    def __init__(self, cliente, servicio, duracion):
        # Comprobar que recibimos un cliente valido
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("El cliente no es valido.")

        # Comprobar que recibimos un servicio valido
        if not isinstance(servicio, Servicios):
            raise ReservaInvalidaError("El servicio no es valido.")

        # Comprobar que la duracion sea positiva
        if (isinstance(duracion, bool) or
                not isinstance(duracion, (int, float)) or
                duracion <= 0):
            raise ReservaInvalidaError(
                "La duracion debe ser un numero mayor a cero."
            )

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    # Confirmar una reserva
    def confirmar(self):
        if self.estado != "Pendiente":
            raise ReservaInvalidaError(
                "Solo se pueden confirmar reservas pendientes."
            )

        self.estado = "Confirmada"
        return self.estado

    # Cancelar una reserva
    def cancelar(self):
        if self.estado not in ("Pendiente", "Confirmada"):
            raise ReservaInvalidaError(
                "Esta reserva no se puede cancelar."
            )

        self.estado = "Cancelada"
        return self.estado

    # Procesar una reserva
    def procesar(self):
        if self.estado != "Confirmada":
            raise ReservaInvalidaError(
                "Primero debe confirmar la reserva."
            )

        self.estado = "Procesada"
        return self.estado

    # Calcular el costo usando el metodo del servicio
    def calcular_total(self):
        try:
            total = self.servicio.calcular_costo(self.duracion)
        except (ValueError, TypeError) as error:
            raise ReservaInvalidaError(
                "No fue posible calcular el costo."
            ) from error
        else:
            return total

    # Mostrar informacion de la reserva
    def mostrar_reserva(self):
        return (
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.obtener_codigo()} | "
            f"Duracion: {self.duracion} horas | "
            f"Estado: {self.estado}"
        )
