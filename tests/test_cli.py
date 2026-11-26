import pytest
from unittest.mock import patch
from src.cli.main import ejecutar_flujo_principal
from src.services.laboratorio_service import LaboratorioService

def test_cli_sesion_completa_y_errores_usuario(capsys):
    """Simula una sesión completa: opciones inválidas, alta, eventos, error de validación, bifurcación y salida."""
    servicio_mem = LaboratorioService.crear_desde_sqlite(":memory:")

    entradas_usuario = [
        "99",                                   # Opción de menú inválida
        "2", "1",                               # Intentar registrar evento sin experimento activo (error controlado)
        "1", "1", "Alonso", "IA", "Principal", "Red Neuronal",  # Alta válida (Investigador + Experimento)
        "2", "1",                               # Evento polimórfico automático
        "2", "2", "",                           # Evento manual vacío (dispara ValueError controlado)
        "3", "2.0",                             # Bifurcación válida
        "4",                                    # Consulta de estado e historial
        "5", "id-que-no-existe",                # Intento de recuperar ID inexistente
        "6"                                     # Salida limpia
    ]

    with patch("builtins.input", side_effect=entradas_usuario):
        with pytest.raises(SystemExit) as exit_info:
            ejecutar_flujo_principal(servicio=servicio_mem)

    assert exit_info.value.code == 0
    salida = capsys.readouterr().out
    assert "Opción no válida" in salida
    assert "Acción denegada" in salida
    assert "Experimento bifurcado y guardado" in salida
    assert "Red Neuronal" in salida