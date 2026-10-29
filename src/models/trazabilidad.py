import uuid
from datetime import datetime

class EventoTrazabilidad:
    def __init__(self, id_experimento: str, id_investigador: str, accion: str):
        self.id_evento = str(uuid.uuid4())
        self.fecha_hora = datetime.now()
        self.id_experimento = id_experimento
        self.id_investigador = id_investigador
        self.accion = accion

    def __str__(self):
        return f"[{self.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')}] {self.accion} (Inv: {self.id_investigador})"