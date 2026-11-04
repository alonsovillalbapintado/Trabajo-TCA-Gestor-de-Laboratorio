import pytest
from src.models.personal import Investigador, Tecnico
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

# --- NUEVAS PRUEBAS: HERENCIA, POLIMORFISMO Y EXCEPCIONES ---

def test_herencia_y_polimorfismo_personal():
    # Creamos dos objetos de clases distintas que heredan del mismo padre
    inv = Investigador("Alonso", "Informática", "Principal")
    tec = Tecnico("Matías", "Mantenimiento", "Mañana")
    
    # Comprobamos la HERENCIA (ambos tienen el atributo id_miembro heredado)
    assert inv.id_miembro is not None
    assert tec.id_miembro is not None
    
    # Comprobamos el POLIMORFISMO (el mismo método actúa de forma diferente)
    assert "diseñando" in inv.ejecutar_tarea()
    assert "calibrando" in tec.ejecutar_tarea()

def test_entrada_invalida_muestra():
    # Comprobamos una ENTRADA INVÁLIDA (consumir cantidad negativa)
    muestra = Muestra("Agua Destilada", "Solvente", 100.0, "ml")
    with pytest.raises(ValueError):
        muestra.consumir_cantidad(-10.0)

def test_demostracion_polimorfismo_coleccion_heterogenea():
    """
    Demuestra polimorfismo puro procesando una lista heterogénea
    de subclases de MiembroLaboratorio.
    """
    # 1. Creación de la lista heterogénea
    equipo_trabajo = [
        Investigador("Dra. Elena", "Genética", "Principal"),
        Tecnico("Carlos", "Mantenimiento", "Tarde"),
        Investigador("Dr. Mario", "Bioquímica", "Asistente")
    ]
    
    # 2. Bucle polimórfico
    resultados = []
    for miembro in equipo_trabajo:
        # Se invoca el mismo método en objetos de clases distintas
        tarea = miembro.ejecutar_tarea()
        resultados.append(tarea)
    
    # 3. Comprobaciones de resultados específicos por subclase
    assert "diseñando el experimento" in resultados[0]
    assert "calibrando el equipamiento" in resultados[1]
    assert "diseñando el experimento" in resultados[2]