from src.persistence.database import ConexionBaseDatos
from src.persistence.repositories import PersonalRepository, ExperimentoRepository
from src.services.laboratorio_service import LaboratorioService

def test_repositorios_y_servicio_en_memoria():
    """Valida la separación entre conexión, repositorios y capa de servicio."""
    db = ConexionBaseDatos(":memory:")
    personal_repo = PersonalRepository(db.conexion)
    exp_repo = ExperimentoRepository(db.conexion, personal_repo)
    servicio = LaboratorioService(exp_repo)

    # 1. Flujo a través de la capa de servicio
    inv = servicio.registrar_personal("1", "Alonso", "Informática", "Principal")
    exp = servicio.crear_experimento("Prueba Arquitectura Limpia", inv)
    servicio.registrar_evento(exp, inv, automatico=False, descripcion="Calibración inicial")

    # 2. Verificación directa en los repositorios
    recuperado = personal_repo.obtener_por_id(inv.id_miembro)
    assert recuperado is not None
    assert recuperado.nombre == "Alonso"

    cursor = db.conexion.cursor()
    cursor.execute("SELECT nombre FROM experimentos WHERE id_experimento = ?", (exp.id_experimento,))
    assert cursor.fetchone()[0] == "Prueba Arquitectura Limpia"

    cursor.execute("SELECT accion FROM trazabilidad WHERE id_experimento = ?", (exp.id_experimento,))
    assert cursor.fetchone()[0] == "Calibración inicial"

    # 3. Probar bifurcación desde el servicio
    exp_v2 = servicio.bifurcar_experimento(exp, "2.0")
    assert exp_v2.version == "2.0"

    db.cerrar()