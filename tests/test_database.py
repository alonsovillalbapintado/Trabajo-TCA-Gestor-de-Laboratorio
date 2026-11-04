import pytest
from src.persistence.database import GestorBaseDatos
from src.models.personal import Investigador
from src.models.experimento import Experimento

def test_guardar_y_recuperar_experimento():
    """Valida que un experimento y su trazabilidad se guardan en SQLite correctamente."""
    # Instanciamos la base de datos en memoria para no afectar al archivo labtrack.db real
    db = GestorBaseDatos(":memory:")
    
    # Preparamos los datos de prueba
    inv = Investigador("Alonso", "Informática", "Principal")
    exp = Experimento("Prueba Cobertura", inv)
    exp.registrar_evento("Calibración inicial de prueba")
    
    # Guardamos en la base de datos
    db.guardar_experimento(exp)
    
    # Verificamos leyendo directamente con SQL
    cursor = db.conexion.cursor()
    
    # 1. Comprobar que el experimento existe
    cursor.execute("SELECT nombre FROM experimentos WHERE id_experimento = ?", (exp.id_experimento,))
    resultado_exp = cursor.fetchone()
    assert resultado_exp is not None
    assert resultado_exp[0] == "Prueba Cobertura"
    
    # 2. Comprobar que la trazabilidad se guardó en cascada
    cursor.execute("SELECT accion FROM trazabilidad WHERE id_experimento = ?", (exp.id_experimento,))
    resultado_evento = cursor.fetchone()
    assert resultado_evento is not None
    assert resultado_evento[0] == "Calibración inicial de prueba"