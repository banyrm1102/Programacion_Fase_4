"""
entidad.py
Clase abstracta base del sistema Software FJ.

Una clase abstracta es una "plantilla": no se puede crear un objeto
directamente de ella, pero sirve para que otras clases (Cliente, Servicio,
Reserva...) hereden lo que tienen en común.
"""

from abc import ABC, abstractmethod


class Entidad(ABC):
    """Representa cualquier cosa importante del sistema (cliente, servicio, reserva)."""

    # Contador compartido por todas las entidades para darles un id único.
    _contador = 0

    def __init__(self):
        Entidad._contador += 1
        self._id = Entidad._contador

    @property
    def id(self):
        """El id solo se puede leer, no cambiar (encapsulación)."""
        return self._id

    @abstractmethod
    def describir(self):
        """Cada clase hija debe explicar cómo se describe a sí misma."""
        pass

    def __str__(self):
        return self.describir()
