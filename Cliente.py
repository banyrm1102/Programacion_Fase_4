""
cliente.py
Clase Cliente: guarda los datos personales y valida cada dato.

Los atributos son privados (llevan doble guion bajo: __nombre) y solo se
modifican a través de propiedades, que revisan que el dato sea válido.
Si un dato es inválido se lanza ClienteInvalidoError (definida en excepciones.py).
"""

import re

from entidad import Entidad
from excepciones import ClienteInvalidoError


class Cliente(Entidad):
    """Cliente de Software FJ."""

    def __init__(self, nombre, correo, telefono):
        # Primero validamos; si algo falla, no se crea el cliente
        # (y tampoco se gasta un id).
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        super().__init__()

    # ---------- Nombre ----------
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ClienteInvalidoError("El nombre es obligatorio y debe ser texto.")
        valor = valor.strip()
        if len(valor) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")
        if any(caracter.isdigit() for caracter in valor):
            raise ClienteInvalidoError("El nombre no puede contener números.")
        self.__nombre = valor.title()

    # ---------- Correo ----------
    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ClienteInvalidoError("El correo es obligatorio y debe ser texto.")
        valor = valor.strip().lower()
        patron = r"^[\w\.\-]+@[\w\-]+(\.[\w\-]+)+$"
        if not re.match(patron, valor):
            raise ClienteInvalidoError(f"El correo '{valor}' no tiene un formato válido.")
        self.__correo = valor

    # ---------- Teléfono ----------
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        texto = str(valor).replace(" ", "").replace("-", "")
        try:
            int(texto)  # Si no es un número, Python lanza ValueError
        except ValueError as error:
            # "from error" encadena las excepciones: se conserva el error original.
            raise ClienteInvalidoError(
                f"El teléfono '{valor}' solo debe tener números."
            ) from error
        if not 7 <= len(texto) <= 10:
            raise ClienteInvalidoError("El teléfono debe tener entre 7 y 10 dígitos.")
        self.__telefono = texto

    # ---------- Métodos de la clase ----------
    def describir(self):
        """Obligatorio: viene de la clase abstracta Entidad."""
        return (
            f"Cliente #{self.id}: {self.nombre} | "
            f"{self.correo} | Tel: {self.telefono}"
        )

    def __repr__(self):
        return f"Cliente(id={self.id}, nombre='{self.nombre}')"
