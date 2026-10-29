import uuid

class Muestra:
    def __init__(self, tipo: str, origen: str, cantidad_disponible: float, unidad_medida: str):
        self.id_muestra = str(uuid.uuid4())
        self.tipo = tipo
        self.origen = origen
        self.cantidad_disponible = cantidad_disponible
        self.unidad_medida = unidad_medida
        
    def consumir_cantidad(self, cantidad: float):
        if cantidad <= self.cantidad_disponible:
            self.cantidad_disponible -= cantidad
        else:
            raise ValueError("No hay suficiente cantidad disponible")