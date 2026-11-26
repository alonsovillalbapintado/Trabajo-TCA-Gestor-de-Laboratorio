import pytest
from src.services.laboratorio_service import LaboratorioService
from src.models.equipamiento import Equipamiento
from src.models.muestra import Muestra

def test_flujo_completo_multisession_persistencia(tmp_path):
    """Valida que todo el estado, trazabilidad y ciclo de vida sobreviven al cierre y reapertura."""
    ruta_db = str(tmp_path / "labtrack_e2e.db")

    # --- SESIÓN 1: Creación, ejecución con equipos/muestras y cierre ---
    servicio_1 = LaboratorioService.crear_desde_sqlite(ruta_db)
    datos = servicio_1.iniciar_nueva_sesion("1", "Alonso", "Bioinformática", "Principal", "Análisis Genómico")
    id_exp = datos["id_experimento"]

    exp = servicio_1.experimento_activo
    exp.iniciar()
    equipo = Equipamiento("Secuenciador", limite_usos_mantenimiento=1)
    muestra = Muestra("Reactivo PCR", cantidad=10.0, unidad="ml", umbral_critico=4.0)

    exp.utilizar_equipamiento(equipo)
    exp.consumir_muestra(muestra, 7.0)
    exp.finalizar(servicio_1.usuario_activo)
    servicio_1.experimento_repo.guardar(exp)
    servicio_1.cerrar()

    # --- SESIÓN 2: Reapertura del sistema desde cero y verificación de recuperación ---
    servicio_2 = LaboratorioService.crear_desde_sqlite(ruta_db)
    resumen = servicio_2.cargar_experimento_en_sesion(id_exp)

    assert resumen["nombre"] == "Análisis Genómico"
    assert resumen["estado"] == "Finalizado"
    assert len(resumen["eventos"]) == 4
    assert any("ALERTA: Equipo enviado automáticamente a mantenimiento" in ev for ev in resumen["eventos"])
    assert any("ALERTA: Stock en nivel crítico" in ev for ev in resumen["eventos"])

    # Verificar que tras recuperar un experimento finalizado sigue protegido frente a mutaciones
    with pytest.raises(ValueError):
        servicio_2.registrar_evento_activo(automatico=False, descripcion="Intento post-cierre")

    servicio_2.cerrar()