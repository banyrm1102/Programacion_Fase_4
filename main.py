
from Cliente import Cliente
from servicios import ServicioSala, ServicioEquipo, ServicioAsesoria
from reserva import Reserva
from excepciones import DatoInvalidoError, ReservaInvalidaError
from logger_config import registrar_evento, registrar_error


# Clase que administra clientes, servicios y reservas
class GestorSoftwareFJ:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, nombre, correo, telefono):
        cliente = Cliente(nombre, correo, telefono)

        # No permitir correos repetidos
        for registrado in self.clientes:
            if registrado.correo == cliente.correo:
                raise DatoInvalidoError("El correo ya esta registrado.")

        self.clientes.append(cliente)
        registrar_evento("Cliente registrado: " + cliente.nombre)
        return cliente

    def registrar_servicio(self, servicio):
        # Validar los datos comunes del servicio
        if not isinstance(servicio, (ServicioSala, ServicioEquipo,
                                     ServicioAsesoria)):
            raise DatoInvalidoError("Tipo de servicio incorrecto.")

        if (isinstance(servicio._tarifa_base, bool) or
                not isinstance(servicio._tarifa_base, (int, float)) or
                servicio._tarifa_base <= 0):
            raise DatoInvalidoError("La tarifa debe ser positiva.")

        if not isinstance(servicio.obtener_codigo(), str) or not servicio.obtener_codigo().strip():
            raise DatoInvalidoError("El codigo del servicio es obligatorio.")

        for registrado in self.servicios:
            if registrado.obtener_codigo() == servicio.obtener_codigo():
                raise DatoInvalidoError("El servicio ya esta registrado.")

        self.servicios.append(servicio)
        registrar_evento("Servicio registrado: " + servicio.obtener_codigo())
        return servicio

    def crear_reserva(self, cliente, servicio, duracion):
        if cliente not in self.clientes:
            raise ReservaInvalidaError("Cliente no registrado.")

        if servicio not in self.servicios:
            raise ReservaInvalidaError("Servicio no registrado.")

        reserva = Reserva(cliente, servicio, duracion)
        reserva.calcular_total()

        self.reservas.append(reserva)
        registrar_evento("Reserva creada correctamente.")
        return reserva


# Ejecutar una prueba sin detener el programa
def ejecutar_prueba(numero, descripcion, funcion, debe_fallar=False):
    print("\nPrueba", numero, "-", descripcion)

    try:
        resultado = funcion()

    except Exception as error:
        registrar_error(
            "Prueba " + str(numero) + ": " + str(error)
        )

        if debe_fallar:
            print("CORRECTO: error controlado:", error)
            return True
        else:
            print("FALLO inesperado:", error)
            return False

    else:
        if debe_fallar:
            print("FALLO: se esperaba detectar un error.")
            return False

        print("CORRECTO:", resultado)
        registrar_evento("Prueba " + str(numero) + " exitosa.")
        return True

    finally:
        print("Prueba finalizada.")


def iniciar_pruebas():
    gestor = GestorSoftwareFJ()
    resultados = []

    print("SISTEMA SOFTWARE FJ")
    print("PRUEBAS DE FUNCIONAMIENTO")

    # 1. Cliente correcto
    resultados.append(ejecutar_prueba(
        1, "Registrar cliente valido",
        lambda: gestor.registrar_cliente(
            "Carlos Perez", "carlos@ejemplo.com", "3001234567"
        )
    ))

    # 2. Cliente sin nombre
    resultados.append(ejecutar_prueba(
        2, "Registrar cliente sin nombre",
        lambda: gestor.registrar_cliente(
            "", "otro@ejemplo.com", "3001234567"
        ), True
    ))

    # 3. Correo incorrecto
    resultados.append(ejecutar_prueba(
        3, "Registrar correo invalido",
        lambda: gestor.registrar_cliente(
            "Maria Lopez", "correo_incorrecto", "3001234567"
        ), True
    ))

    # 4. Cliente duplicado
    resultados.append(ejecutar_prueba(
        4, "Registrar correo repetido",
        lambda: gestor.registrar_cliente(
            "Pedro Gomez", "carlos@ejemplo.com", "3009876543"
        ), True
    ))

    # Crear los servicios para las siguientes pruebas
    sala = ServicioSala("S01", "Sala de reuniones", 50000, 10)
    equipo = ServicioEquipo("E01", "Computador", 30000, 10000)
    asesoria = ServicioAsesoria("A01", "Asesoria", 40000, "Senior")

    # 5, 6 y 7. Registrar servicios
    resultados.append(ejecutar_prueba(
        5, "Registrar sala",
        lambda: gestor.registrar_servicio(sala)
    ))

    resultados.append(ejecutar_prueba(
        6, "Registrar equipo",
        lambda: gestor.registrar_servicio(equipo)
    ))

    resultados.append(ejecutar_prueba(
        7, "Registrar asesoria",
        lambda: gestor.registrar_servicio(asesoria)
    ))

    # 8. Servicio con tarifa incorrecta
    resultados.append(ejecutar_prueba(
        8, "Registrar servicio con tarifa negativa",
        lambda: gestor.registrar_servicio(
            ServicioSala("S02", "Sala incorrecta", -5000, 10)
        ), True
    ))

    # Utilizar el cliente registrado en la prueba 1
    cliente = gestor.clientes[0]

    # 9. Reserva valida
    resultados.append(ejecutar_prueba(
        9, "Crear reserva correcta",
        lambda: gestor.crear_reserva(cliente, sala, 2)
    ))

    reserva = gestor.reservas[0]

    # 10. Reserva con duracion incorrecta
    resultados.append(ejecutar_prueba(
        10, "Crear reserva con duracion negativa",
        lambda: gestor.crear_reserva(cliente, sala, -2),
        True
    ))

    # 11. Confirmar reserva
    resultados.append(ejecutar_prueba(
        11, "Confirmar reserva",
        lambda: reserva.confirmar()
    ))

    # 12. Procesar reserva
    resultados.append(ejecutar_prueba(
        12, "Procesar reserva",
        lambda: reserva.procesar()
    ))

    # 13. Intentar cancelar una reserva procesada
    resultados.append(ejecutar_prueba(
        13, "Cancelar reserva ya procesada",
        lambda: reserva.cancelar(),
        True
    ))

    # 14. Calcular costo con descuento e impuesto
    resultados.append(ejecutar_prueba(
        14, "Calcular costo con descuento e impuesto",
        lambda: sala.calcular_costo(2, impuesto=19, descuento=10)
    ))

    # Mostrar el resumen final
    correctas = sum(resultados)

    print("\nRESUMEN FINAL")
    print("Pruebas realizadas:", len(resultados))
    print("Pruebas correctas:", correctas)
    print("Pruebas fallidas:", len(resultados) - correctas)

    if correctas == len(resultados):
        print("TODAS LAS PRUEBAS FUERON SUPERADAS")
    else:
        print("HAY PRUEBAS QUE NECESITAN CORRECCION")


if __name__ == "__main__":
    iniciar_pruebas()
