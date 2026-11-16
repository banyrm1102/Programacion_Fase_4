
import logging

# Nombre del archivo donde se guardaran los eventos
LOG_FILENAME = "registro_eventos.log"

# Crear el logger del sistema
logger = logging.getLogger("SoftwareFJ")
logger.setLevel(logging.DEBUG)

# Evitar agregar el mismo manejador varias veces
if not logger.handlers:
    archivo = logging.FileHandler(
        LOG_FILENAME,
        encoding="utf-8"
    )

    formato = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    archivo.setFormatter(formato)
    logger.addHandler(archivo)


# Registrar operaciones realizadas correctamente
def registrar_evento(mensaje):
    logger.info(mensaje)


# Registrar errores del sistema
def registrar_error(mensaje):
    logger.error(mensaje)
