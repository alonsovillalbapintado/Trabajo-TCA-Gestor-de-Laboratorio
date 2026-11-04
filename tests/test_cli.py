import pytest
from unittest.mock import patch
from src.cli.main import ejecutar_flujo_principal

@patch('builtins.input', side_effect=['5']) # Simulamos que el usuario teclea '5' en el menú
@patch('sys.exit') # Interceptamos sys.exit para que pytest no se cierre abruptamente
def test_cli_opcion_salir(mock_exit, mock_input):
    """
    Prueba que el menú principal arranca la base de datos, 
    muestra las opciones y sale limpiamente al pulsar 5.
    Esto aumenta drásticamente la cobertura del archivo main.py.
    """
    ejecutar_flujo_principal()
    
    # Verificamos que el programa intentó salir con código 0 (éxito)
    mock_exit.assert_called_once_with(0)