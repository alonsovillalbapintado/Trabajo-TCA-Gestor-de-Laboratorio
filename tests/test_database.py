import sqlite3

import pytest

from src.models.personal import Tecnico
from src.persistence.database import ConexionBaseDatos
from src.persistence.repositories import ExperimentoRepository, PersonalRepository
from src.services.laboratorio_service import LaboratorioService


def test_recuperacion_completa_agregado_y_polimorfismo():
    """Verifica el ciclo completo guardar -> recuperar reconstruyendo subclase e historial ordenado."""
    db = ConexionBaseDatos(":memory:")
    personal_repo = PersonalRepository(db.conexion)
    exp_repo = ExperimentoRepository(db.conexion, personal_repo)
    servicio = LaboratorioService(exp_repo)

    tec = servicio.registrar_personal("2", "Matías", "Instrumentación", "Noche")
    exp = servicio.crear_experimento("Cromatografía Líquida", tec)
    servicio.registrar_evento(exp, tec, automatico=True)
    servicio.registrar_evento(
        exp, tec, automatico=False, descripcion="Ajuste de presión"
    )
    exp.iniciar()
    exp_repo.guardar(exp)

    # Recuperación desde cero a partir del ID
    recuperado = exp_repo.obtener_por_id(exp.id_experimento)
    assert recuperado is not None
    assert recuperado.nombre == "Cromatografía Líquida"
    assert recuperado.estado == "En curso"
    assert isinstance(recuperado.investigador_principal, Tecnico)
    assert recuperado.investigador_principal.turno == "Noche"
    assert len(recuperado.historial_eventos) == 3
    assert recuperado.historial_eventos[1].accion == "Ajuste de presión"

    db.cerrar()


def test_busqueda_inexistente_y_clave_foranea():
    """Valida respuestas ante registros inexistentes y protección de integridad referencial."""
    db = ConexionBaseDatos(":memory:")
    personal_repo = PersonalRepository(db.conexion)
    exp_repo = ExperimentoRepository(db.conexion, personal_repo)

    assert personal_repo.obtener_por_id("uuid-inexistente") is None
    assert exp_repo.obtener_por_id("uuid-inexistente") is None

    # Intentar insertar un experimento apuntando a un responsable no persistido debe fallar
    cursor = db.conexion.cursor()
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute(
            "INSERT INTO experimentos VALUES ('exp-1', 'Test FK', '1.0', 'En preparación', 'usuario-fantasma')"
        )

    db.cerrar()
