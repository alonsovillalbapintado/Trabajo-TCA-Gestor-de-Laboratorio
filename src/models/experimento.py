import uuid
import copy
from src.models.trazabilidad import EventoTrazabilidad

class Experimento:
    def __init__(self, nombre: str, investigador_principal):
        self.id_experimento = str(uuid.uuid4())
        self.nombre = nombre
        self.version = "1.0"
        self.investigador_principal = investigador_principal
        self.muestras_usadas = []
        self.equipos_usados = []
        self.historial_eventos = []
        self.estado = "En preparación"

    def registrar_evento(self, accion: str):
        # Crea un evento y lo añade al historial propio del experimento
        evento = EventoTrazabilidad(self.id_experimento, self.investigador_principal.id_investigador, accion)
        self.historial_eventos.append(evento)

    def bifurcar_version(self, nueva_version: str):
        # Hace una copia profunda para no perder el historial anterior
        nuevo_experimento = copy.deepcopy(self)
        nuevo_experimento.id_experimento = str(uuid.uuid4())
        nuevo_experimento.version = nueva_version
        nuevo_experimento.estado = f"Bifurcado de {self.version}"
        return nuevo_experimento