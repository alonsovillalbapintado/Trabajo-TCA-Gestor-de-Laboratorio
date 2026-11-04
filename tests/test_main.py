import pytest
from src.models.personal import Investigador, Tecnico
from src.models.experimento import Experimento
from src.models.muestra import Muestra
from src.models.equipamiento import Equipamiento

# ==========================================
# 1. PRUEBAS DE HERENCIA Y POLIMORFISMO
# ==========================================
def test_polimorfismo_personal():
    """Valida que distintas subclases ejecuten tareas de forma polimórfica."""
    inv = Investigador("Alonso", "Informática", "Principal")
    tec = Tecnico("Matías", "Mantenimiento", "Mañana")
    
    assert "diseñando" in inv.ejecutar_tarea()
    assert "calibrando" in tec.ejecutar_tarea()

# ==========================================
# 2. PRUEBAS DE CASOS LÍMITE
# ==========================================
def test_caso_limite_consumir_toda_la_muestra():
    """Caso límite: Consumir EXACTAMENTE el 100% del stock disponible, dejando 0."""
    muestra = Muestra("Reactivo A", "Químico", 100.0, "ml")
    muestra.consumir_cantidad(100.0) 
    assert muestra.cantidad_disponible == 0.0

# ==========================================
# 3. ENTRADAS INVÁLIDAS Y EXCEPCIONES
# ==========================================
def test_excepcion_consumo_excesivo():
    """Comportamiento de excepciones: Intentar gastar más de lo que hay."""
    muestra = Muestra("Alcohol", "Solvente", 50.0, "ml")
    with pytest.raises(ValueError, match="No hay suficiente cantidad"):
        muestra.consumir_cantidad(60.0)

def test_entrada_invalida_cantidad_negativa():
    """Entrada inválida: Introducir un número negativo al consumir."""
    muestra = Muestra("Agua", "Solvente", 50.0, "ml")
    with pytest.raises(ValueError, match="mayor que 0"):
        muestra.consumir_cantidad(-10.0)

# ==========================================
# 4. ESCENARIOS ALTERNATIVOS Y TRAZABILIDAD
# ==========================================
def test_escenario_alternativo_bifurcar_sin_eventos():
    """Escenario alternativo: Bifurcar un experimento que aún está vacío."""
    inv = Investigador("Alonso", "Informática")
    exp = Experimento("Prueba Base", inv)
    
    exp_v2 = exp.bifurcar_version("2.0")
    
    assert exp_v2.version == "2.0"
    assert len(exp_v2.historial_eventos) == 0
    assert exp_v2.id_experimento != exp.id_experimento

def test_trazabilidad_con_polimorfismo():
    """Comprueba que el polimorfismo interactúa bien con la trazabilidad."""
    inv = Investigador("Matías", "Química")
    exp = Experimento("Experimento 1", inv)
    
    # Al ejecutar la tarea polimórfica, el evento se debe autoguardar
    accion = exp.asignar_y_ejecutar_tarea(inv)
    
    assert len(exp.historial_eventos) == 1
    assert exp.historial_eventos[0].accion == accion
    assert exp.historial_eventos[0].id_investigador == inv.id_miembro