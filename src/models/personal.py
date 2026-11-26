import uuid
from abc import ABC, abstractmethod


class MiembroLaboratorio(ABC):
    """Superclase abstracta con invariantes de identidad y políticas de autorización."""

    def __init__(self, nombre: str, especialidad: str):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del miembro del laboratorio es obligatorio.")
        if not especialidad or not especialidad.strip():
            raise ValueError(
                "La especialidad del miembro del laboratorio es obligatoria."
            )

        self.id_miembro = str(uuid.uuid4())
        self.nombre = nombre.strip()
        self.especialidad = especialidad.strip()

    @abstractmethod
    def ejecutar_tarea(self) -> str:
        pass

    def puede_aprobar_experimento(self) -> bool:
        """Por defecto, ningún perfil puede aprobar o cerrar experimentos salvo que lo autorice."""
        return False

    def puede_calibrar_equipo(self) -> bool:
        """Por defecto, ningún perfil realiza mantenimiento técnico salvo que lo autorice."""
        return False


class Investigador(MiembroLaboratorio):
    def __init__(self, nombre: str, especialidad: str, rol: str = "Principal"):
        super().__init__(nombre, especialidad)
        self.rol = rol.strip() if rol and rol.strip() else "Principal"

    def ejecutar_tarea(self) -> str:
        return f"Investigador {self.nombre} ({self.rol}) diseñando protocolo y validando hipótesis"

    def puede_aprobar_experimento(self) -> bool:
        return True


class Tecnico(MiembroLaboratorio):
    def __init__(self, nombre: str, especialidad: str, turno: str = "Mañana"):
        super().__init__(nombre, especialidad)
        if not turno or not turno.strip():
            raise ValueError("El turno del técnico no puede estar vacío.")
        self.turno = turno.strip()

    def ejecutar_tarea(self) -> str:
        return f"Técnico {self.nombre} (Turno: {self.turno}) calibrando instrumental y preparando reactivos"

    def puede_calibrar_equipo(self) -> bool:
        return True
