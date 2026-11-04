import pytest
from unittest.mock import patch
from src.cli.main import ejecutar_flujo_principal

@patch('builtins.input', side_effect=['5'])
def test_cli_opcion_salir(mock_input):
    """
    Prueba que el menú principal arranca la base de datos, 
    muestra las opciones y sale limpiamente al pulsar 5.
    Atrapa el SystemExit para romper el bucle infinito del menú de forma segura.
    """
    # Verificamos que al elegir '5', el programa lanza la excepción de salida del sistema
    with pytest.raises(SystemExit) as exit_info:
        ejecutar_flujo_principal()
    
    # Comprobamos que el código de salida es 0 (cierre exitoso y limpio)
    assert exit_info.value.code == 0