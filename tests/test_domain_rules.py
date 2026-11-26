import pytest

from src.models.equipamiento import Equipamiento
from src.models.experimento import Experimento
from src.models.muestra import Muestra
from src.models.personal import Investigador, Tecnico
from src.models.trazabilidad import EventoTrazabilidad


def test_equipamiento_desgaste_y_mantenimiento():
    equipo = Equipamiento("Espectrómetro UV", limite_usos_mantenimiento=2)
    assert equipo.esta_disponible() is True

    equipo.registrar_uso()
    assert equipo.usos_acumulados == 1
    assert equipo.esta_disponible() is True

    # Al alcanzar el límite de usos pasa automáticamente a mantenimiento
    equipo.registrar_uso()
    assert equipo.estado == "En mantenimiento"
    assert equipo.esta_disponible() is False

    # No permite usarse mientras está en mantenimiento
    with pytest.raises(ValueError):
        equipo.registrar_uso()

    # Completar mantenimiento reinicia el contador y lo deja disponible
    equipo.completar_mantenimiento()
    assert equipo.esta_disponible() is True
    assert equipo.usos_acumulados == 0


def test_muestra_contaminacion_y_umbral_critico():
    muestra = Muestra("Reactivo A", cantidad=12.0, unidad="ml", umbral_critico=5.0)
    muestra.consumir(8.0)
    assert muestra.cantidad == 4.0
    assert muestra.esta_en_nivel_critico() is True

    muestra.marcar_contaminada()
    with pytest.raises(ValueError):
        muestra.consumir(1.0)
    with pytest.raises(ValueError):
        muestra.reponer(10.0)


def test_inmutabilidad_evento_trazabilidad():
    evento = EventoTrazabilidad("Calibración inicial", "uuid-123")
    with pytest.raises(AttributeError):
        evento.accion = "Acción manipulada"


def test_ciclo_vida_y_permisos_experimento():
    inv = Investigador("Alonso", "Bioinformática", "Principal")
    tec = Tecnico("Matías", "Instrumentación", "Mañana")
    exp = Experimento("Secuenciación Genómica", inv)
    equipo = Equipamiento("Secuenciador NGS", limite_usos_mantenimiento=3)
    muestra = Muestra("ADN Muestra 1", cantidad=20.0, unidad="ul", umbral_critico=5.0)

    exp.iniciar()
    assert exp.estado == "En curso"

    exp.utilizar_equipamiento(equipo)
    exp.consumir_muestra(muestra, 16.0)
    assert muestra.esta_en_nivel_critico() is True

    # Un técnico no tiene permisos para finalizar el experimento
    with pytest.raises(ValueError):
        exp.finalizar(tec)

    # Un investigador sí puede finalizarlo
    exp.finalizar(inv)
    assert exp.estado == "Finalizado"

    # Invariante: un experimento finalizado bloquea cualquier modificación posterior
    with pytest.raises(ValueError):
        exp.registrar_evento("Intento de modificación tardía")
