import uuid


class Equipamiento:
    """Entidad de dominio con máquina de estados y control de desgaste operativo."""

    ESTADOS_VALIDOS = ("Disponible", "En uso", "En mantenimiento", "Fuera de servicio")

    def __init__(
        self,
        nombre: str,
        estado: str = "Disponible",
        limite_usos_mantenimiento: int = 5,
    ):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del equipamiento no puede estar vacío.")
        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError(
                f"Estado '{estado}' no válido. Permitidos: {self.ESTADOS_VALIDOS}"
            )
        if limite_usos_mantenimiento <= 0:
            raise ValueError(
                "El límite de usos para mantenimiento debe ser mayor que cero."
            )

        self.id_equipamiento = str(uuid.uuid4())
        self.nombre = nombre.strip()
        self._estado = estado
        self._usos_acumulados = 0
        self.limite_usos_mantenimiento = limite_usos_mantenimiento

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def usos_acumulados(self) -> int:
        return self._usos_acumulados

    def esta_disponible(self) -> bool:
        return self._estado == "Disponible"

    def registrar_uso(self):
        """Aplica la regla de negocio: solo equipos disponibles pueden usarse y se bloquean al alcanzar su límite."""
        if not self.esta_disponible():
            raise ValueError(
                f"El equipo '{self.nombre}' no puede utilizarse (estado actual: {self._estado})."
            )

        self._usos_acumulados += 1
        if self._usos_acumulados >= self.limite_usos_mantenimiento:
            self._estado = "En mantenimiento"

    def enviar_a_mantenimiento(self):
        if self._estado == "En mantenimiento":
            raise ValueError(
                f"El equipo '{self.nombre}' ya se encuentra en mantenimiento."
            )
        self._estado = "En mantenimiento"

    def completar_mantenimiento(self):
        """Restaura la operatividad del equipo y reinicia su contador de desgaste."""
        if self._estado != "En mantenimiento":
            raise ValueError(f"El equipo '{self.nombre}' no está en mantenimiento.")
        self._usos_acumulados = 0
        self._estado = "Disponible"
