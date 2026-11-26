from src.models.personal import Investigador, Tecnico, MiembroLaboratorio
from src.models.experimento import Experimento
from src.persistence.repositories import ExperimentoRepository
from src.services.logger import get_logger

class LaboratorioService:
    """Capa de aplicación: orquesta casos de uso, dominio y persistencia."""

    def __init__(self, experimento_repo: ExperimentoRepository):
        self.experimento_repo = experimento_repo
        self.logger = get_logger()

    def registrar_personal(self, tipo_opcion: str, nombre: str, especialidad: str, detalle: str) -> MiembroLaboratorio:
        if tipo_opcion == "2":
            return Tecnico(nombre, especialidad, detalle)
        return Investigador(nombre, especialidad, detalle or "Principal")

    def crear_experimento(self, nombre_exp: str, responsable: MiembroLaboratorio) -> Experimento:
        experimento = Experimento(nombre_exp, responsable)
        self.experimento_repo.guardar(experimento)
        self.logger.info(f"Experimento creado y persistido: {experimento.id_experimento}")
        return experimento

    def registrar_evento(self, experimento: Experimento, miembro: MiembroLaboratorio, automatico: bool, descripcion: str = "") -> str:
        if automatico:
            accion = experimento.asignar_y_ejecutar_tarea(miembro)
        else:
            experimento.registrar_evento(descripcion)
            accion = descripcion

        self.experimento_repo.guardar(experimento)
        self.logger.info(f"Evento registrado en experimento {experimento.id_experimento}: {accion}")
        return accion

    def bifurcar_experimento(self, experimento: Experimento, nueva_version: str) -> Experimento:
        nuevo_experimento = experimento.bifurcar_version(nueva_version)
        self.experimento_repo.guardar(nuevo_experimento)
        self.logger.info(f"Experimento bifurcado a versión {nueva_version} (ID: {nuevo_experimento.id_experimento})")
        return nuevo_experimento