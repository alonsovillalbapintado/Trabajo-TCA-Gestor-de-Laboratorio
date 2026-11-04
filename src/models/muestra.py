import uuid

class Muestra:
    def __init__(self, tipo: str, origen: str, cantidad_disponible: float, unidad_medida: str):
        self.id_muestra = str(uuid.uuid4())
        self.tipo = tipo
        self.origen = origen
        self.cantidad_disponible = cantidad_disponible
        self.unidad_medida = unidad_medida
        
    def consumir_cantidad(self, cantidad: float):
        if cantidad <= 0:
            raise ValueError("La cantidad a consumir debe ser mayor que 0.")
        if cantidad > self.cantidad_disponible:
            raise ValueError("No hay suficiente cantidad.")
        self.cantidad_disponible -= cantidad