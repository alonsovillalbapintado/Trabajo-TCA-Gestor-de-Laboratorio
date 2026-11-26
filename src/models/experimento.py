import uuid
import copy
from src.models.personal import MiembroLaboratorio
from src.models.trazabilidad import EventoTrazabilidad
from src.models.equipamiento import Equipamiento
from src.models.muestra import Muestra

class Experimento:
    """Agregado raíz que gobierna el ciclo de vida, recursos y trazabilidad del experimento."""

    ESTADOS_CERRADOS = ("Finalizado", "Cancelado")

    def __init__(self, nombre: str, investigador_principal: MiembroLaboratorio, version: str = "1.0"):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del experimento no puede estar vacío.")
        if not isinstance(investigador_principal, MiembroLaboratorio):
            raise ValueError("Debe asignarse un MiembroLaboratorio válido como responsable.")

        self.id_experimento = str(uuid.uuid4())
        self.nombre = nombre.strip()
        self.investigador_principal = investigador_principal
        self.version = version
        self.estado = "En preparación"
        self.historial_eventos: list[EventoTrazabilidad] = []

    def _verificar_experimento_abierto(self):
        """Invariante: un experimento finalizado o cancelado es inmutable."""
        if self.estado in self.ESTADOS_CERRADOS:
            raise ValueError(f"Operación denegada: el experimento '{self.nombre}' está en estado '{self.estado}'.")

    def iniciar(self):
        if self.estado != "En preparación":
            raise ValueError(f"Solo se puede iniciar un experimento 'En preparación' (actual: {self.estado}).")
        self.estado = "En curso"
        self.registrar_evento("Inicio formal de ejecución experimental", self.investigador_principal.id_miembro)

    def finalizar(self, miembro: MiembroLaboratorio):
        """Regla de negocio: solo perfiles autorizados pueden cerrar un experimento abierto."""
        self._verificar_experimento_abierto()
        if not miembro.puede_aprobar_experimento():
            raise ValueError(f"Permiso denegado: {miembro.nombre} ({miembro.__class__.__name__}) no puede finalizar experimentos.")
        self.estado = "Finalizado"
        self.historial_eventos.append(
            EventoTrazabilidad(f"Experimento finalizado y validado por {miembro.nombre}", miembro.id_miembro)
        )

    def cancelar(self, motivo: str):
        self._verificar_experimento_abierto()
        if not motivo or not motivo.strip():
            raise ValueError("Debe especificarse un motivo para cancelar el experimento.")
        self.estado = "Cancelado"
        self.historial_eventos.append(
            EventoTrazabilidad(f"Experimento cancelado. Motivo: {motivo.strip()}", self.investigador_principal.id_miembro)
        )

    def registrar_evento(self, accion: str, id_miembro: str | None = None):
        self._verificar_experimento_abierto()
        responsable_id = id_miembro or self.investigador_principal.id_miembro
        evento = EventoTrazabilidad(accion, responsable_id)
        self.historial_eventos.append(evento)

    def asignar_y_ejecutar_tarea(self, miembro: MiembroLaboratorio) -> str:
        self._verificar_experimento_abierto()
        resultado = miembro.ejecutar_tarea()
        self.registrar_evento(resultado, miembro.id_miembro)
        return resultado

    def utilizar_equipamiento(self, equipo: Equipamiento):
        """Coordina el uso del equipo y registra automáticamente su impacto en la trazabilidad."""
        self._verificar_experimento_abierto()
        equipo.registrar_uso()
        aviso = " [ALERTA: Equipo enviado automáticamente a mantenimiento]" if not equipo.esta_disponible() else ""
        self.registrar_evento(f"Uso de equipamiento '{equipo.nombre}'{aviso}")

    def consumir_muestra(self, muestra: Muestra, cantidad: float):
        """Coordina el descuento de stock de la muestra y registra alertas de umbral crítico."""
        self._verificar_experimento_abierto()
        muestra.consumir(cantidad)
        alerta = " [ALERTA: Stock en nivel crítico]" if muestra.esta_en_nivel_critico() else ""
        self.registrar_evento(f"Consumo de {cantidad} {muestra.unidad} de '{muestra.nombre}'{alerta}")

    def bifurcar_version(self, nueva_version: str) -> "Experimento":
        if not nueva_version or not nueva_version.strip():
            raise ValueError("La nomenclatura de la nueva versión no puede estar vacía.")
        if nueva_version.strip() == self.version:
            raise ValueError("La nueva versión debe ser distinta a la versión actual.")

        clon = copy.deepcopy(self)
        clon.id_experimento = str(uuid.uuid4())
        clon.version = nueva_version.strip()
        clon.estado = "En preparación"
        clon.historial_eventos.append(
            EventoTrazabilidad(
                f"Bifurcación creada desde versión {self.version} -> {clon.version}",
                self.investigador_principal.id_miembro
            )
        )
        return clon