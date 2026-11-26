from src.models.personal import Investigador, Tecnico, MiembroLaboratorio
from src.models.experimento import Experimento
from src.models.trazabilidad import EventoTrazabilidad

class PersonalRepository:
    """Acceso a datos exclusivo para la entidad MiembroLaboratorio."""

    def __init__(self, conexion):
        self.conexion = conexion

    def guardar(self, miembro: MiembroLaboratorio):
        tipo = miembro.__class__.__name__
        atributo_extra = getattr(miembro, "turno", None) or getattr(miembro, "rol", None)
        cursor = self.conexion.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO personal (id_miembro, tipo, nombre, especialidad, atributo_extra)
            VALUES (?, ?, ?, ?, ?)
        """, (miembro.id_miembro, tipo, miembro.nombre, miembro.especialidad, atributo_extra))
        self.conexion.commit()

    def obtener_por_id(self, id_miembro: str) -> MiembroLaboratorio | None:
        cursor = self.conexion.cursor()
        cursor.execute(
            "SELECT tipo, nombre, especialidad, atributo_extra FROM personal WHERE id_miembro = ?",
            (id_miembro,)
        )
        fila = cursor.fetchone()
        if not fila:
            return None

        tipo, nombre, especialidad, extra = fila
        miembro = (
            Tecnico(nombre, especialidad, extra or "Mañana")
            if tipo == "Tecnico"
            else Investigador(nombre, especialidad, extra or "Principal")
        )
        miembro.id_miembro = id_miembro
        return miembro


class ExperimentoRepository:
    """Acceso a datos exclusivo para Experimento y su trazabilidad."""

    def __init__(self, conexion, personal_repo: PersonalRepository):
        self.conexion = conexion
        self.personal_repo = personal_repo

    def guardar(self, experimento: Experimento):
        self.personal_repo.guardar(experimento.investigador_principal)

        cursor = self.conexion.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO experimentos (id_experimento, nombre, version, estado, id_miembro_responsable)
            VALUES (?, ?, ?, ?, ?)
        """, (
            experimento.id_experimento,
            experimento.nombre,
            experimento.version,
            experimento.estado,
            experimento.investigador_principal.id_miembro
        ))

        cursor.execute("DELETE FROM trazabilidad WHERE id_experimento = ?", (experimento.id_experimento,))
        for evento in experimento.historial_eventos:
            accion = getattr(evento, "accion", str(evento))
            id_miembro = getattr(evento, "id_miembro", experimento.investigador_principal.id_miembro)
            cursor.execute("""
                INSERT INTO trazabilidad (id_experimento, id_miembro, accion)
                VALUES (?, ?, ?)
            """, (experimento.id_experimento, id_miembro, accion))

        self.conexion.commit()

    def obtener_por_id(self, id_experimento: str) -> Experimento | None:
        """Reconstruye el agregado completo (experimento, responsable polimórfico e historial)."""
        cursor = self.conexion.cursor()
        cursor.execute(
            "SELECT nombre, version, estado, id_miembro_responsable FROM experimentos WHERE id_experimento = ?",
            (id_experimento,)
        )
        fila = cursor.fetchone()
        if not fila:
            return None

        nombre, version, estado, id_responsable = fila
        responsable = self.personal_repo.obtener_por_id(id_responsable)
        if not responsable:
            return None

        experimento = Experimento(nombre, responsable, version=version)
        experimento.id_experimento = id_experimento
        experimento.estado = estado

        cursor.execute(
            "SELECT id_miembro, accion FROM trazabilidad WHERE id_experimento = ? ORDER BY id_evento ASC",
            (id_experimento,)
        )
        for id_miembro_ev, accion in cursor.fetchall():
            experimento.historial_eventos.append(EventoTrazabilidad(accion, id_miembro_ev))

        return experimento

    def listar_ids(self) -> list[str]:
        cursor = self.conexion.cursor()
        cursor.execute("SELECT id_experimento FROM experimentos")
        return [fila[0] for fila in cursor.fetchall()]