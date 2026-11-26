import uuid

class Muestra:
    """Entidad de dominio con control de stock, integridad biológica y alertas de reposición."""

    def __init__(self, nombre: str, *args, **kwargs):
        if not nombre or not str(nombre).strip():
            raise ValueError("El nombre de la muestra no puede estar vacío.")

        tipo = kwargs.get("tipo", "General")
        unidad = kwargs.get("unidad", "unidades")
        umbral_critico = kwargs.get("umbral_critico", 5.0)
        cantidad = kwargs.get("cantidad", None)

        numeros = []
        textos = []
        for arg in args:
            if isinstance(arg, bool):
                continue
            try:
                numeros.append(float(arg))
            except (ValueError, TypeError):
                textos.append(str(arg))

        if cantidad is None:
            if not numeros:
                raise ValueError("Debe especificarse una cantidad numérica para la muestra.")
            cantidad = numeros[0]
            if len(numeros) > 1 and "umbral_critico" not in kwargs:
                umbral_critico = numeros[1]

        if len(textos) == 1 and "unidad" not in kwargs:
            unidad = textos[0]
        elif len(textos) >= 2:
            if "tipo" not in kwargs:
                tipo = textos[0]
            if "unidad" not in kwargs:
                unidad = textos[1]

        if float(cantidad) < 0:
            raise ValueError("La cantidad inicial de una muestra no puede ser negativa.")

        self.id_muestra = str(uuid.uuid4())
        self.nombre = str(nombre).strip()
        self.tipo = tipo
        self._cantidad = float(cantidad)
        self.unidad = unidad
        self.umbral_critico = float(umbral_critico)
        self._contaminada = False

    @property
    def cantidad(self) -> float:
        return self._cantidad

    @property
    def cantidad_disponible(self) -> float:
        return self._cantidad

    @property
    def contaminada(self) -> bool:
        return self._contaminada

    def consumir(self, cantidad_a_consumir: float):
        """Valida integridad, positividad y disponibilidad antes de descontar stock."""
        if self._contaminada:
            raise ValueError(f"Operación denegada: la muestra '{self.nombre}' está marcada como contaminada.")
        if cantidad_a_consumir <= 0:
            raise ValueError("La cantidad a consumir debe ser mayor que 0.")
        if cantidad_a_consumir > self._cantidad:
            raise ValueError(
                f"No hay suficiente cantidad en '{self.nombre}': solicitado {cantidad_a_consumir} {self.unidad}, "
                f"disponible {self._cantidad} {self.unidad}."
            )
        self._cantidad -= cantidad_a_consumir

    def consumir_cantidad(self, cantidad_a_consumir: float):
        """Alias de compatibilidad con la interfaz original de Muestra."""
        self.consumir(cantidad_a_consumir)

    def reponer(self, cantidad_extra: float):
        if self._contaminada:
            raise ValueError(f"No se puede reponer stock sobre una muestra contaminada ('{self.nombre}').")
        if cantidad_extra <= 0:
            raise ValueError("La cantidad a reponer debe ser mayor que 0.")
        self._cantidad += cantidad_extra

    def marcar_contaminada(self):
        """Inutiliza la muestra de forma irreversible por seguridad biológica/química."""
        self._contaminada = True

    def esta_en_nivel_critico(self) -> bool:
        return self._cantidad <= self.umbral_critico