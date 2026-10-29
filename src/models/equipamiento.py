import uuid

class Equipamiento:
    def __init__(self, nombre: str, estado: str = "Disponible"):
        self.id_equipo = str(uuid.uuid4())
        self.nombre = nombre
        self.estado = estado
        self.historial_mantenimiento = []
        
    def cambiar_estado(self, nuevo_estado: str):
        self.estado = nuevo_estado