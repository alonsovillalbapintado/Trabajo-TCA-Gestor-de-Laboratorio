import uuid
from abc import ABC, abstractmethod

# 1. CLASE BASE ABSTRACTA (Superclase)
class MiembroLaboratorio(ABC):
    def __init__(self, nombre: str, especialidad: str):
        self.id_miembro = str(uuid.uuid4())
        self.nombre = nombre
        self.especialidad = especialidad

    # Este método abstracto obliga a las clases hijas a sobrescribirlo (Polimorfismo)
    @abstractmethod
    def ejecutar_tarea(self) -> str:
        pass

# 2. CLASE HIJA 1: Investigador
class Investigador(MiembroLaboratorio):
    def __init__(self, nombre: str, especialidad: str, rol: str = "Principal"):
        # Llama al constructor de la clase padre
        super().__init__(nombre, especialidad)
        self.rol = rol

    # Se sobrescribe el método del padre
    def ejecutar_tarea(self) -> str:
        return f"El investigador {self.nombre} ({self.rol}) está diseñando el experimento."

# 3. CLASE HIJA 2: Tecnico (Nueva entidad para demostrar herencia)
class Tecnico(MiembroLaboratorio):
    def __init__(self, nombre: str, especialidad: str, turno: str):
        super().__init__(nombre, especialidad)
        self.turno = turno

    # Se sobrescribe el método del padre de forma distinta
    def ejecutar_tarea(self) -> str:
        return f"El técnico {self.nombre} (Turno: {self.turno}) está calibrando el equipamiento." 