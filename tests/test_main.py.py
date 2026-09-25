import pytest
from src.main import procesar_opcion

def test_procesar_opcion_valida():
    """Prueba de humo: Verifica que una opción válida devuelva el flujo correcto."""
    resultado = procesar_opcion("1")
    assert "creación de experimentos" in resultado.lower()

def test_procesar_opcion_invalida():
    """Prueba de humo: Verifica el manejo de una opción incorrecta."""
    resultado = procesar_opcion("99")
    assert resultado == "Opción no válida. Intente de nuevo."