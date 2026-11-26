from src.models.experimento import Experimento
from src.models.personal import Investigador, MiembroLaboratorio, Tecnico
from src.persistence.database import ConexionBaseDatos
from src.persistence.repositories import ExperimentoRepository, PersonalRepository
from src.services.logger import get_logger


class LaboratorioService:
    """Capa de aplicación: gestiona casos de uso, estado de sesión, dominio y persistencia."""

    def __init__(
        self,
        experimento_repo: ExperimentoRepository,
        db_conexion: ConexionBaseDatos | None = None,
    ):
        self.experimento_repo = experimento_repo
        self.db_conexion = db_conexion
        self.logger = get_logger()
        self.usuario_activo: MiembroLaboratorio | None = None
        self.experimento_activo: Experimento | None = None

    @classmethod
    def crear_desde_sqlite(cls, db_path: str = "labtrack.db") -> "LaboratorioService":
        """Fábrica de infraestructura: aísla a la capa CLI de conocer SQLite o los repositorios."""
        db = ConexionBaseDatos(db_path)
        personal_repo = PersonalRepository(db.conexion)
        experimento_repo = ExperimentoRepository(db.conexion, personal_repo)
        return cls(experimento_repo, db_conexion=db)

    def _verificar_sesion_activa(self) -> tuple[Experimento, MiembroLaboratorio]:
        if not self.experimento_activo or not self.usuario_activo:
            raise ValueError(
                "No hay ningún experimento activo en la sesión. Crea o carga uno primero."
            )
        return self.experimento_activo, self.usuario_activo

    def registrar_personal(
        self, tipo_opcion: str, nombre: str, especialidad: str, detalle: str
    ) -> MiembroLaboratorio:
        if tipo_opcion == "2":
            return Tecnico(nombre, especialidad, detalle)
        return Investigador(nombre, especialidad, detalle or "Principal")

    def crear_experimento(
        self, nombre_exp: str, responsable: MiembroLaboratorio
    ) -> Experimento:
        experimento = Experimento(nombre_exp, responsable)
        self.experimento_repo.guardar(experimento)
        self.usuario_activo = responsable
        self.experimento_activo = experimento
        self.logger.info(
            f"Experimento creado y persistido: {experimento.id_experimento}"
        )
        return experimento

    def iniciar_nueva_sesion(
        self,
        tipo_personal: str,
        nombre: str,
        especialidad: str,
        detalle: str,
        nombre_exp: str,
    ) -> dict:
        responsable = self.registrar_personal(
            tipo_personal, nombre, especialidad, detalle
        )
        experimento = self.crear_experimento(nombre_exp, responsable)
        return {
            "perfil": responsable.__class__.__name__,
            "responsable": responsable.nombre,
            "experimento": experimento.nombre,
            "id_experimento": experimento.id_experimento,
        }

    def cargar_experimento_en_sesion(self, id_experimento: str) -> dict:
        """Recupera un experimento persistido en base de datos y restaura la sesión."""
        experimento = self.experimento_repo.obtener_por_id(id_experimento.strip())
        if not experimento:
            raise ValueError(f"No existe ningún experimento con ID '{id_experimento}'.")
        self.experimento_activo = experimento
        self.usuario_activo = experimento.investigador_principal
        self.logger.info(
            f"Experimento recuperado en sesión: {experimento.id_experimento}"
        )
        return self.obtener_resumen_sesion()

    def registrar_evento_activo(self, automatico: bool, descripcion: str = "") -> str:
        experimento, miembro = self._verificar_sesion_activa()
        return self.registrar_evento(
            experimento, miembro, automatico=automatico, descripcion=descripcion
        )

    def registrar_evento(
        self,
        experimento: Experimento,
        miembro: MiembroLaboratorio,
        automatico: bool,
        descripcion: str = "",
    ) -> str:
        if automatico:
            accion = experimento.asignar_y_ejecutar_tarea(miembro)
        else:
            experimento.registrar_evento(descripcion)
            accion = descripcion

        self.experimento_repo.guardar(experimento)
        self.logger.info(
            f"Evento registrado en experimento {experimento.id_experimento}: {accion}"
        )
        return accion

    def bifurcar_experimento_activo(self, nueva_version: str) -> Experimento:
        experimento, _ = self._verificar_sesion_activa()
        nuevo = self.bifurcar_experimento(experimento, nueva_version)
        self.experimento_activo = nuevo
        return nuevo

    def bifurcar_experimento(
        self, experimento: Experimento, nueva_version: str
    ) -> Experimento:
        nuevo_experimento = experimento.bifurcar_version(nueva_version)
        self.experimento_repo.guardar(nuevo_experimento)
        self.logger.info(
            f"Experimento bifurcado a versión {nueva_version} (ID: {nuevo_experimento.id_experimento})"
        )
        return nuevo_experimento

    def obtener_resumen_sesion(self) -> dict:
        experimento, miembro = self._verificar_sesion_activa()
        return {
            "id": experimento.id_experimento,
            "nombre": experimento.nombre,
            "version": experimento.version,
            "responsable": f"{miembro.nombre} ({miembro.especialidad})",
            "estado": experimento.estado,
            "eventos": [str(ev) for ev in experimento.historial_eventos],
        }

    def cerrar(self):
        if self.db_conexion:
            self.db_conexion.cerrar()
        self.logger.info("Cierre limpio de la aplicación y liberación de recursos.")

    def generar_informe_markdown(
        self, ruta_salida: str = "informe_experimento.md"
    ) -> str:
        """Genera un informe automático en Markdown con el estado y trazabilidad del experimento activo."""
        datos = self.obtener_resumen_sesion()
        lineas = [
            f"# Informe Técnico de Experimento: {datos['nombre']}",
            "",
            f"- **ID Único (UUID):** `{datos['id']}`",
            f"- **Versión:** `{datos['version']}`",
            f"- **Estado Actual:** `{datos['estado']}`",
            f"- **Responsable:** {datos['responsable']}",
            "",
            "## Registro Inmutable de Trazabilidad",
            "",
        ]
        if not datos["eventos"]:
            lineas.append("_Sin eventos registrados._")
        else:
            for ev in datos["eventos"]:
                lineas.append(f"- {ev}")

        contenido = "\n".join(lineas) + "\n"
        with open(ruta_salida, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)

        self.logger.info(f"Informe automático exportado en '{ruta_salida}'.")
        return ruta_salida
