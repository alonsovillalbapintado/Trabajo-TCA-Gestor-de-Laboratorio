import uuid

class Muestra:
    """Entidad de dominio con control de stock, integridad biológica y alertas de reposición."""

    def __init__(self, nombre: str, cantidad: float, unidad: str = "unidades", umbral_critico: float = 5.0):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la muestra no puede estar vacío.")
        if cantidad < 0:
            raise ValueError("La cantidad inicial de una muestra no puede ser negativa.")

        self.id_muestra = str(uuid.uuid4())
        self.nombre = nombre.strip()
        self._cantidad = float(cantidad)
        self.unidad = unidad
        self.umbral_critico = float(umbral_critico)
        self._contaminada = False

    @property
    def cantidad(self) -> float:
        return self._cantidad

    @property
    def contaminada(self) -> bool:
        return self._contaminada

    def consumir(self, cantidad_a_consumir: float):
        """Valida integridad, positividad y disponibilidad antes de descontar stock."""
        if self._contaminada:
            raise ValueError(f"Operación denegada: la muestra '{self.nombre}' está marcada como contaminada.")
        if cantidad_a_consumir <= 0:
            raise ValueError("La cantidad a consumir debe ser estrictamente positiva.")
        if cantidad_a_consumir > self._cantidad:
            raise ValueError(
                f"Stock insuficiente en '{self.nombre}': solicitado {cantidad_a_consumir} {self.unidad}, "
                f"disponible {self._cantidad} {self.unidad}."
            )
        self._cantidad -= cantidad_a_consumir

    def reponer(self, cantidad_extra: float):
        if self._contaminada:
            raise ValueError(f"No se puede reponer stock sobre una muestra contaminada ('{self.nombre}').")
        if cantidad_extra <= 0:
            raise ValueError("La cantidad a reponer debe ser mayor que cero.")
        self._cantidad += cantidad_extra

    def marcar_contaminada(self):
        """Inutiliza la muestra de forma irreversible por seguridad biológica/química."""
        self._contaminada = True

    def esta_en_nivel_critico(self) -> bool:
        return self._cantidad <= self.umbral_critico