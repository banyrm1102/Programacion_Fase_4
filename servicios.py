"""
Pilar de la abstraccion en python
Utiliza el metodo 'abc' para definir contratos e implemebtaciones desacopladas"""

from abc import ABC, abstractmethod

class Servicios(ABC):
    """
    Clase Abstracta que define el contrato comun de servicio
    no puede ser instanciada directamente.
    """
    
    def __init__(self, codigo, descripcion_base, tarifa_base)->None:
        # Atributos encapsulados comunes para cualquier tipo de servicio
        self._codigo=codigo
        self._descripcion_base=descripcion_base
        self._tarifa_base=tarifa_base
    
    # Método getter para obtener el código
    def obtener_codigo(self):
        return self._codigo
    
    # Método común para describir el servicio
    def describir_servicio(self):
        return f"Servicio Código: {self._codigo} | {self._descripcion_base} (Tarifa base: ${self._tarifa_base})"
    
    # 1. Método abstracto para validar parámetros (obligatorio para las clases hijas)
    @abstractmethod
    def validar_parametros(self, horas):
        pass

    # 2. Método abstracto principal
    @abstractmethod
    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):
        pass
    
#CLASES HIJAS

#PRIMERA CLASE HIJA

class ServicioSala(Servicios): #Clase para reserva de salas 
    def __init__(self, codigo, descripcion_base, tarifa_base, capacidad_personas):
        super().__init__(codigo, descripcion_base, tarifa_base) #Llama al constructor de la clase Servicios
        self.capacidad_personas = capacidad_personas
        
    #Sobreescribe los metodos abstractos de Servicios  
    def validar_parametros(self, horas):
        #Si no hay un valor valido de hora, lanza un valueError
        if horas <= 0:
            raise ValueError("Las horas de reserva de la sala deben ser mayores a 0.")
        return True

    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):
        self.validar_parametros(horas)
        
        # Cálculo base
        subtotal = horas * self._tarifa_base
        
        # Aplicar descuento y luego impuestos
        monto_descuento = subtotal * (descuento / 100)
        subtotal_con_descuento = subtotal - monto_descuento
        
        monto_impuesto = subtotal_con_descuento * (impuesto / 100)
        total_final = subtotal_con_descuento + monto_impuesto
        
        return total_final
    
#SEGUNDA CLASE HIJA
class ServicioEquipo(Servicios): #Clase que simula el alquier de equipos 
    
    def __init__(self, codigo, descripcion_base, tarifa_base, costo_seguro_fijo):
        super().__init__(codigo, descripcion_base, tarifa_base)
        self.costo_seguro_fijo = costo_seguro_fijo 
        """
        costo_seguro_fijo es un atributo unico, el seguro es un recargo al alquiler de un equipo por 
        mantenimiento del equipo independiente de las horas que se alquiló"""
                
    #Sobreescribe los metodos de Servicios
    def validar_parametros(self, horas):
        #Si no hay un valor valido de hora (horas menor o igual a 0), lanza un valueError 
        if horas <= 0:
            raise ValueError("El tiempo de alquiler del equipo debe ser mayor a 0 horas.")
        return True

    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):
        self.validar_parametros(horas)
        
        #El costo incluye las horas por la tarifa más un seguro fijo del equipo
    
        subtotal = (horas * self._tarifa_base) + self.costo_seguro_fijo
        
        monto_descuento = subtotal * (descuento / 100) #Se calcula la cantidad exacta de dinero que se le va a restar al costo inicial
        subtotal_con_descuento = subtotal - monto_descuento #Se aplica el descuento restándoselo al subtotal original.
        
        monto_impuesto = subtotal_con_descuento * (impuesto / 100) 
        """Se calcula el valor del impuesto (como el IVA) pero únicamente 
        sobre el subtotal que ya tiene el descuento aplicado (y no sobre el precio inflado original)."""
        total_final = subtotal_con_descuento + monto_impuesto #Se suma el subtotal con descuento más el valor del impuesto calculado.
        
        return total_final
    
class ServicioAsesoria(Servicios):
        def __init__(self, codigo, descripcion_base, tarifa_base, nivel_especialidad):
            super().__init__(codigo, descripcion_base, tarifa_base)
            self.nivel_especialidad = nivel_especialidad # Ej: "Junior", "Senior"
            #Atributo unico, la especialidad de quien va atomar la tutoria
            
#Sobreescribe los metodos
        def validar_parametros(self, horas):
            if horas <= 0 or horas > 8:
                raise ValueError("Las asesorías especializadas deben ser entre 1 y 8 horas por sesión.")
            return True

        def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):
            self.validar_parametros(horas)
        
        # Si es especialidad Senior, la tarifa base podría multiplicarse por un factor (Mayor costo del servicio)
            if self.nivel_especialidad.lower()== "senior":
                factor = 1.5 
            else:
                factor = 1.0 
                
            subtotal = (horas * self._tarifa_base) * factor
        
            monto_descuento = subtotal * (descuento / 100)
            subtotal_con_descuento = subtotal - monto_descuento
        
            monto_impuesto = subtotal_con_descuento * (impuesto / 100)
            total_final = subtotal_con_descuento + monto_impuesto
        
            return total_final
        
        
#EJEMPLO DE INSTANCIA PARA COMPROBAR SU FUNCIONAMIENTO 

# 1. Instancias el objeto pasando los datos que pide el __init__ de ServicioSala:
# (codigo, descripcion_base, tarifa_base, capacidad_personas)
sala_juntas = ServicioSala("SALA-101", "Sala de Juntas Ejecutiva", 50.0, 10)

# 2. Muestras la descripción general llamando al método heredado
print(sala_juntas.describir_servicio())

# 3. Calculas el costo llamando al método y pasándole las horas, impuesto y descuento
try:
    # (horas=4, impuesto=19.0, descuento=10.0)
    costo_total = sala_juntas.calcular_costo(horas=4, impuesto=19.0, descuento=10.0)
    print(f"Costo total a pagar: ${costo_total}")
    
except ValueError as e:
    print(f"Error de validación: {e}")