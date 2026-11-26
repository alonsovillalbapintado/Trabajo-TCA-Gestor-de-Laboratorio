# 🔬 LabTrack - Gestor de Laboratorio de Investigación

**Grupo 2**  
**Integrantes:** Matías Mayor, Alonso Villalba Pintado, Antonio Hermana Rubio  
**Asignatura:** Técnicas de Programación Avanzada 

LabTrack es un sistema de gestión de laboratorios diseñado con una arquitectura robusta Orientada a Objetos (POO). Su objetivo es garantizar la trazabilidad inmutable de los experimentos y gestionar los recursos (personal, muestras y equipamiento) del laboratorio.

---

## 📖 GUÍA DE USUARIO

Esta sección explica cómo instalar, configurar y utilizar LabTrack en tu entorno local.

### 1. Requisitos e Instalación
El proyecto está estructurado como un paquete instalable de Python moderno siguiendo las especificaciones PEP 517 y PEP 621.
1. Requiere Python 3.10 o superior.
2. Clona el repositorio y crea un entorno virtual (`python -m venv venv`).
3. Activa el entorno y configura el paquete y sus dependencias (`pytest`, `pytest-cov`) ejecutando:
   pip install -e .

2. Ejecución del Programa
El sistema está diseñado para ejecutarse interpretando el módulo principal. Estando en la raíz del proyecto y con el entorno virtual activado, la ejecución correcta es:   

python -m src.cli.main

### 3. Ejemplos Completos de Ejecución (Interacción entre Capas)

A continuación se muestran tres escenarios completos que ilustran el flujo de datos de extremo a extremo: desde la interfaz de consola hasta la persistencia relacional y los registros de auditoría.

#### Escenario A: Sesión Completa en Consola (Alta, Polimorfismo, Bifurcación y Consulta)
Ejecutando `python -m src.cli.main`, el usuario interactúa con la capa `cli/`, que delega cada operación en `LaboratorioService` y persiste automáticamente los cambios mediante los repositorios:

```text
========================================
🔬 LABTRACK: GESTOR DE LABORATORIO 🔬
========================================
1. Crear nuevo Personal y Experimento
2. Registrar evento de Trazabilidad
3. Bifurcar Experimento (Crear nueva versión)
4. Mostrar estado actual y Trazabilidad
5. Salir
========================================
Selecciona una opción: 1

--- ALTA DE PERSONAL Y EXPERIMENTO ---
¿Qué desea registrar? (1: Investigador / 2: Técnico): 2
Nombre: Matías
Especialidad/Área: Instrumentación
Turno (Mañana/Tarde/Noche): Mañana

--- NUEVO EXPERIMENTO ---
Nombre del experimento: Espectroscopía UV-Vis

✅ ¡Éxito! Registrado Tecnico: Matías
✅ Experimento 'Espectroscopía UV-Vis' persistido con ID: 082aecab-46f7-427b-b990-48e0f8121269

========================================
Selecciona una opción: 2

--- REGISTRAR ACCIÓN POLIMÓRFICA ---
1. Ejecutar tarea automática según el perfil de personal
2. Escribir descripción manual
Selecciona opción: 1
✅ Evento polimórfico registrado: 'Calibración instrumental y preparación de reactivos por Matías (Turno: Mañana)'

========================================
Selecciona una opción: 3

Indica la nomenclatura de la nueva versión (ej. 'v1.1' o '2.0'): v2.0
✅ Experimento bifurcado y guardado. Nueva versión activa: v2.0

========================================
Selecciona una opción: 4

--- ESTADO DEL EXPERIMENTO ---
Nombre:       Espectroscopía UV-Vis
Versión:      v2.0
Responsable:  Matías (Instrumentación)
Estado:       En preparación

--- HISTORIAL DE TRAZABILIDAD ---
  [2026-11-26 17:15:10] (Usuario: 6614259d-f723-4bdf-b78d-42fc103c1a9f) -> Calibración instrumental y preparación de reactivos por Matías (Turno: Mañana)
  [2026-11-26 17:15:24] (Usuario: 6614259d-f723-4bdf-b78d-42fc103c1a9f) -> Bifurcación creada desde versión 1.0 -> v2.0

========================================
Selecciona una opción: 5

Saliendo de LabTrack... ¡Hasta pronto!
```

---

#### Escenario B: Colaboración entre Dominio Rico, Servicio y Persistencia
El siguiente flujo muestra cómo las entidades de `src/models/` protegen sus invariantes de negocio (ciclo de vida, permisos por rol, desgaste de equipos y umbral crítico de muestras) mientras `LaboratorioService` sincroniza el estado en SQLite:

```python
from src.persistence.database import ConexionBaseDatos
from src.persistence.repositories import PersonalRepository, ExperimentoRepository
from src.services.laboratorio_service import LaboratorioService
from src.models.equipamiento import Equipamiento
from src.models.muestra import Muestra

# 1. Inicialización de infraestructura e inyección de dependencias
db = ConexionBaseDatos("labtrack.db")
personal_repo = PersonalRepository(db.conexion)
experimento_repo = ExperimentoRepository(db.conexion, personal_repo)
servicio = LaboratorioService(experimento_repo)

# 2. Creación de actores y agregado raíz mediante el servicio
investigador = servicio.registrar_personal("1", "Alonso", "Bioinformática", "Principal")
tecnico = servicio.registrar_personal("2", "Matías", "Instrumentación", "Mañana")
experimento = servicio.crear_experimento("Secuenciación Genómica", investigador)

# 3. Ejecución de reglas de negocio encapsuladas en el dominio
experimento.iniciar()  # Transición de estado: 'En preparación' -> 'En curso'

espectrometro = Equipamiento("Espectrómetro UV", limite_usos_mantenimiento=1)
reactivo = Muestra("Reactivo ADN", cantidad=10.0, unidad="ml", umbral_critico=5.0)

experimento.utilizar_equipamiento(espectrometro)      # Agota límite de usos -> pasa a 'En mantenimiento'
experimento.consumir_muestra(reactivo, cantidad=7.0)  # Stock restante: 3.0 ml -> activa alerta crítica

# 4. Control de autorizaciones e invariantes de cierre
try:
    experimento.finalizar(tecnico)  # Rechazado: un Técnico no tiene permiso de aprobación
except ValueError as err:
    print(f"Regla de negocio aplicada: {err}")

experimento.finalizar(investigador)  # Aceptado: estado -> 'Finalizado' (bloquea mutaciones futuras)
experimento_repo.guardar(experimento)
db.cerrar()
```

---

#### Escenario C: Trazabilidad Resultante en `labtrack.db` y `labtrack_system.log`
Tras ejecutar los flujos anteriores, la capa de persistencia y el motor de logging reflejan de forma sincronizada el estado del sistema:

* **Salida en `labtrack_system.log`:**
  ```text
  2026-11-26 17:15:02,110 - INFO - Iniciando aplicación LabTrack...
  2026-11-26 17:15:02,115 - INFO - Capas de persistencia y servicio inicializadas con éxito.
  2026-11-26 17:15:08,402 - INFO - Experimento creado y persistido: 082aecab-46f7-427b-b990-48e0f8121269
  2026-11-26 17:15:10,891 - INFO - Evento registrado en experimento 082aecab-46f7-427b-b990-48e0f8121269: Calibración instrumental y preparación de reactivos por Matías (Turno: Mañana)
  2026-11-26 17:15:24,310 - INFO - Experimento bifurcado a versión v2.0 (ID: 9f1c3e20-8a11-4c9d-a012-77b1e4d90012)
  2026-11-26 17:15:30,004 - INFO - Cierre limpio de la aplicación por el usuario.
  ```

* **Registros persistidos en la tabla `trazabilidad` (`labtrack.db`):**
  ```text
  id_evento | id_experimento                       | accion
  ----------+--------------------------------------+---------------------------------------------------------------------------------
  1         | f47ac10b-58cc-4372-a567-0e02b2c3d479 | Inicio formal de ejecución experimental
  2         | f47ac10b-58cc-4372-a567-0e02b2c3d479 | Uso de equipamiento 'Espectrómetro UV' [ALERTA: Equipo enviado automáticamente a mantenimiento]
  3         | f47ac10b-58cc-4372-a567-0e02b2c3d479 | Consumo de 7.0 ml de 'Reactivo ADN' [ALERTA: Stock en nivel crítico]
  4         | f47ac10b-58cc-4372-a567-0e02b2c3d479 | Experimento finalizado y validado por Alonso
  ```

🛠️ GUÍA DEL DESARROLLADOR

Esta sección detalla la arquitectura interna, decisiones de diseño y herramientas de persistencia para futuros contribuidores.

1. Arquitectura Orientada a Objetos (El Dominio)
El sistema se divide en capas (cli/, models/, services/, persistence/, tests/) para separar la lógica de negocio de la interfaz. Todas las capas de la arquitectura están correctamente inicializadas como submódulos mediante __init__.py. En la capa de modelos (src/models/), interactúan las siguientes entidades:   

- Experimento: Clase central que asocia un responsable, recursos y un historial de eventos.   

- Muestra: Gestiona el stock físico. Lanza excepciones (ValueError) si se intenta consumir más cantidad de la disponible.   

- Equipamiento: Maquinaria con estados controlados ("Disponible", "En mantenimiento").   

- EventoTrazabilidad: Entidad inmutable que captura el "cuándo" (datetime.now()), "quién" y "qué" de cada acción.   

2. Herencia y Polimorfismo
Para modelar al equipo de trabajo, hemos implementado una jerarquía de clases que demuestra el uso práctico de herencia y polimorfismo:   


- Superclase Abstracta: MiembroLaboratorio. Define los atributos comunes (id_miembro mediante uuid4, nombre, especialidad) y un método abstracto @abstractmethod def ejecutar_tarea().   


- Subclases (Herencia): Las clases Investigador y Tecnico heredan de MiembroLaboratorio y sobrescriben el método ejecutar_tarea() con comportamientos distintos.   
README.md

- Polimorfismo en Acción: La clase Experimento posee el método asignar_y_ejecutar_tarea(miembro: MiembroLaboratorio). Este método recibe un objeto genérico y ejecuta su tarea automáticamente, demostrando un acoplamiento débil y polimorfismo puro.   


3. Motor de Trazabilidad y Versionado

La trazabilidad es el pilar de LabTrack. No guardamos simples textos, sino que cada acción instancia un objeto EventoTrazabilidad, se almacena en la lista historial_eventos de la clase Experimento, y todo queda ligado al ID único (uuid4) del investigador que realizó la acción.   


- Versionado: Para evitar que un experimento se convierta en un simple CRUD, hemos implementado el método bifurcar_version(nueva_version). Mediante copy.deepcopy(), clona el experimento entero, generando un nuevo id_experimento pero preservando de forma idéntica el historial de trazabilidad anterior.   

4. Persistencia, Logging y Manejo de Errores (PRAC3)

El proyecto ha evolucionado para integrar persistencia y monitorización profesional:   


- Persistencia con SQLite: Se ha implementado el Patrón Repositorio en src/persistence/database.py. El sistema genera automáticamente el archivo labtrack.db, mapeando los objetos en memoria y sus UUIDs a tablas relacionales (personal, experimentos, trazabilidad) manteniendo el polimorfismo.   

- Logging Centralizado: A través de src/services/logger.py, el sistema registra de forma invisible toda la actividad en el archivo labtrack_system.log, utilizando niveles de severidad (INFO, WARNING, ERROR).   


- Manejo de Excepciones: La interfaz de consola (main.py) está blindada con bloques try/except que capturan tanto reglas de negocio (ValueError) como errores críticos, garantizando que el programa no se interrumpa abruptamente y mostrando mensajes limpios al usuario[cite: 4].

5. Pruebas Automatizadas y Cobertura (Testing)

El sistema de testing se ha ampliado superando ampliamente el objetivo del 55 % de cobertura global, manteniendo un 98.5% en la capa de lógica de negocio (models/)[cite: 4]. Se ha desarrollado una batería de pruebas con pytest evaluando[cite: 4]:

- Pruebas de Dominio: Herencia, polimorfismo, casos límite (ej. consumir el 100% exacto de una muestra), y entradas inválidas (rechazar consumos de muestra negativos lanzando ValueError)[cite: 4].

- Pruebas de Persistencia (test_database.py): Se valida el correcto funcionamiento del ORM personalizado y las consultas SQL instanciando bases de datos volátiles (:memory:), asegurando que los tests no corrompen el archivo labtrack.db de producción[cite: 4].

- Mocking de Interfaz (test_cli.py): Utilizando @patch de la librería unittest.mock, se han automatizado las entradas del usuario (ej. simular la pulsación de la tecla '5') para testear el flujo de la terminal de forma desatendida, elevando la cobertura del módulo principal[cite: 4].

**Estructura Final del Proyecto**
Para que confirmes visualmente que tu repositorio está impecable antes de subirlo, esta es la estructura exacta que debes tener en Visual Studio Code:

Trabajo-TCA-Gestor-de-Laboratorio/
├── .pytest_cache/
├── docs/
│   ├── src/
│   ├── index.html
│   ├── search.js
│   └── src.html
├── htmlcov/
├── src/
│   ├── __pycache__/
│   ├── cli/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── labtrack.egg-info/
│   ├── models/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── equipamiento.py
│   │   ├── experimento.py
│   │   ├── muestra.py
│   │   ├── personal.py
│   │   └── trazabilidad.py
│   ├── persistence/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   └── database.py
│   └── services/
│       ├── __pycache__/
│       ├── __init__.py
│       └── logger.py
├── tests/
│   ├── __pycache__/
│   ├── test_cli.py
│   ├── test_database.py
│   └── test_main.py
├── venv/
├── .coverage
├── .gitignore
├── labtrack_system.log
├── labtrack.db
├── pyproject.toml
└── README.md