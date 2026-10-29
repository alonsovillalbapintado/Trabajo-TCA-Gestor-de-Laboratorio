import uuid

class Investigador:
    def __init__(self, nombre: str, especialidad: str, rol: str):
        self.id_investigador = str(uuid.uuid4())
        self.nombre = nombre
        self.especialidad = especialidad
        self.rol = rol