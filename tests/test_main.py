import pytest
from src.models.investigador import Investigador
from src.models.experimento import Experimento
from src.models.muestra import Muestra
from src.models.equipamiento import Equipamiento

def test_crear_investigador():
    inv = Investigador("Alonso", "Informática", "Principal")
    assert inv.nombre == "Alonso"
    assert inv.especialidad == "Informática"
    assert inv.id_investigador is not None

def test_logica_muestra_consumo():
    muestra = Muestra("Reactivo A", "Sintético", 100.0, "ml")
    assert muestra.cantidad_disponible == 100.0
    
    # Consumir una cantidad válida
    muestra.consumir_cantidad(30.0)
    assert muestra.cantidad_disponible == 70.0
    
    # Intentar consumir más de lo que hay debe lanzar un error
    with pytest.raises(ValueError, match="No hay suficiente cantidad"):
        muestra.consumir_cantidad(100.0)

def test_estado_equipamiento():
    equipo = Equipamiento("Microscopio Electrónico")
    assert equipo.estado == "Disponible"
    
    equipo.cambiar_estado("En mantenimiento")
    assert equipo.estado == "En mantenimiento"

def test_crear_y_trazabilidad_experimento():
    inv = Investigador("Matías", "Química", "Asistente")
    exp = Experimento("Prueba de estrés", inv)
    
    assert exp.nombre == "Prueba de estrés"
    assert exp.version == "1.0"
    assert len(exp.historial_eventos) == 0
    
    # Registrar un evento
    exp.registrar_evento("Muestra calentada a 50 grados")
    assert len(exp.historial_eventos) == 1
    assert exp.historial_eventos[0].accion == "Muestra calentada a 50 grados"

def test_bifurcar_version_experimento():
    inv = Investigador("Alonso", "Informática", "Principal")
    exp_original = Experimento("Algoritmo Genético", inv)
    exp_original.registrar_evento("Inicio de pruebas")
    
    # Bifurcar
    exp_v2 = exp_original.bifurcar_version("2.0")
    
    assert exp_v2.version == "2.0"
    assert exp_v2.id_experimento != exp_original.id_experimento
    # Comprobar que el historial se ha copiado correctamente
    assert len(exp_v2.historial_eventos) == 1