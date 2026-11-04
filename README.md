# 🔬 LabTrack - Gestor de Laboratorio de Investigación

**Grupo 2**  
**Integrantes:** Matías Mayor, Alonso Villalba Pintado, Antonio Hermana Rubio  
**Asignatura:** Técnicas de Programación Avanzada (PRAC2 y PRAC3)  

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

3. Ejemplos de Uso (Flujo de Consola CLI)
El programa se ejecuta interactuando con la terminal. A continuación, un ejemplo real de ejecución:   

========================================
🔬 LABTRACK: GESTOR DE LABORATORIO 🔬
========================================
1. Crear nuevo Personal y Experimento
2. Registrar evento de Trazabilidad
3. Mostrar estado actual y Trazabilidad

> Selecciona una opción: 1
--- ALTA DE PERSONAL Y EXPERIMENTO ---
¿Qué desea registrar? (1: Investigador / 2: Técnico): 2
Nombre: Matías
Especialidad/Área: Mantenimiento
Turno (Mañana/Tarde/Noche): Mañana

✅ ¡Éxito! Registrado Tecnico: Matías
✅ Experimento 'Calibración A1' creado con ID: f82d1c9a-3b21-4f1e...

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
├── .pytest_cache/             <-- (Caché de ejecución de pytest)
├── docs/                      <-- (Documentación HTML autogenerada)
│   ├── src/
│   ├── index.html
│   ├── search.js
│   └── src.html
├── htmlcov/                   <-- (Reporte visual web de la cobertura de código)
├── src/
│   ├── __pycache__/           <-- (Bytecode compilado por Python para mayor velocidad)
│   ├── cli/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── labtrack.egg-info/     <-- (Metadatos del empaquetado tras hacer pip install -e .)
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
├── venv/                      <-- (Entorno virtual aislado con las dependencias)
│   ├── Include/
│   ├── Lib/
│   ├── Scripts/
│   ├── testing/
│   ├── .gitignore
│   └── pyvenv.cfg
├── .coverage                  <-- (Archivo de datos generado por pytest-cov)
├── .gitignore                 <-- (Reglas de exclusión para no subir basura a GitHub)
├── labtrack_system.log        <-- (Registro invisible de sistema y errores)
├── labtrack.db                <-- (Base de datos SQLite principal)
├── pyproject.toml             <-- (Configuración estándar del paquete PEP 517)
└── README.md                  <-- (Documentación global del proyecto)