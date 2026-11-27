# 🔬 LabTrack — Gestor de Laboratorio de Investigación

**Asignatura:** Técnicas de Programación Avanzada (2026–2027) — Universidad Nebrija  
**Grupo:** Grupo 2  
**Integrantes:** Matías Mayor, Alonso Villalba Pintado, Antonio Hermana Rubio  
**Versión:** `v1.0.0` (Entrega Final — PRAC4) | **Licencia:** MIT  

---

## 1. Visión General

**LabTrack** es una aplicación en Python diseñada para gestionar el ciclo de vida completo de experimentos científicos en un laboratorio de investigación. El sistema garantiza la **trazabilidad inmutable** de todas las operaciones realizadas sobre muestras, equipamiento y versiones de experimentos, almacenando los datos de forma persistente en **SQLite**.

El proyecto está construido sobre una **arquitectura en cuatro capas** (`CLI` $\rightarrow$ `Services` $\rightarrow$ `Models` $\leftarrow$ `Persistence`) aplicando principios SOLID (especialmente Responsabilidad Única e Inyección de Dependencias), un modelo de dominio rico con máquinas de estado e invariantes encapsulados, registro centralizado de auditoría (`logging`), informes técnicos automáticos en Markdown, pruebas automatizadas con un **88 % de cobertura** e integración continua mediante **GitHub Actions**.

---

## 2. Requisitos, Instalación y Seguridad

### Requisitos Previos
* **Python 3.10 o superior** (validado en Python 3.12 y 3.14).
* El núcleo de ejecución de la aplicación utiliza exclusivamente la **biblioteca estándar de Python** (`sqlite3`, `uuid`, `logging`, `abc`, `datetime`, `copy`), por lo que no requiere dependencias externas en producción.

### Instalación Paso a Paso (PEP 517 / PEP 621)
El empaquetado (`pyproject.toml`) separa estrictamente las dependencias de ejecución (`dependencies = []`) de las herramientas de desarrollo y auditoría (`[project.optional-dependencies] dev`):

1. **Clonar el repositorio y entrar en la carpeta raíz:**
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd Trabajo-TCA-Gestor-de-Laboratorio
   ```

2. **Crear y activar el entorno virtual (`venv`):**
   ```bash
   python -m venv venv

   # En Windows (PowerShell):
   .\venv\Scripts\activate

   # En Linux / macOS:
   source venv/bin/activate
   ```

3. **Instalar el paquete según el perfil de uso:**
   * **Modo Usuario (ejecución limpia sin librerías de prueba):**
     ```bash
     python -m pip install -e .
     ```
   * **Modo Desarrollador / Evaluador (incluye `pytest`, `pytest-cov`, `pdoc`, `black` y `ruff`):**
     ```bash
     python -m pip install -e ".[dev]"
     ```

### Configuración y Nota de Seguridad
* El archivo `.env.example` en la raíz documenta las variables de configuración admitidas (`LABTRACK_DB_PATH`, `LABTRACK_LOG_FILE`, `LABTRACK_LOG_LEVEL`).
* **Nota de seguridad:** No se suben credenciales, claves privadas, archivos `.env` ni bases de datos locales (`*.db`, `*.log`) al repositorio. Todos ellos están excluidos explícitamente mediante `.gitignore`.

---

## 3. Ejecución, Modo Demo y Documentación

Desde la raíz del proyecto con el entorno virtual `(venv)` activado:

* **Iniciar la aplicación interactiva (CLI):**
  ```bash
  python -m src.cli.main
  ```
  *(También disponible mediante el entry point configurado en `pyproject.toml`: `labtrack`)*.

* **Ejecutar el Modo Demo automático (validación rápida en aula):**
  ```bash
  python -m src.cli.main --demo
  ```
  Ejecuta de forma desatendida un flujo completo sobre base de datos en memoria (alta de personal y experimento, desgaste automático de equipamiento, alerta crítica de stock, bifurcación de versión y exportación de `informe_demo.md`).

* **Ejecutar la batería de pruebas y reporte de cobertura:**
  ```bash
  python -m pytest --cov=src tests/
  ```

* **Generar la documentación técnica de la API (`pdoc`):**
  ```bash
  python -m pdoc src -o docs
  ```
  La documentación HTML resultante es navegable abriendo `docs/index.html` en cualquier navegador web.

---

## 4. Ejemplos Completos de Ejecución (Interacción entre Capas)

### Escenario A: Sesión Completa en Consola (`python -m src.cli.main`)
Muestra la interacción del usuario creando personal y un experimento, registrando tareas polimórficas, bifurcando versiones, consultando el historial y recuperando sesiones persistidas en SQLite:

```text
==========================================
🔬 LABTRACK: GESTOR DE LABORATORIO 🔬
==========================================
1. Crear nuevo Personal y Experimento
2. Registrar evento de Trazabilidad
3. Bifurcar Experimento (Crear nueva versión)
4. Mostrar estado actual y Trazabilidad
5. Recuperar Experimento existente por ID
6. Salir
==========================================
Selecciona una opción: 1

--- ALTA DE PERSONAL Y EXPERIMENTO ---
¿Qué desea registrar? (1: Investigador / 2: Técnico): 2
Nombre: Matías
Especialidad/Área: Instrumentación
Turno (Mañana/Tarde/Noche): Mañana
Nombre del experimento: Espectroscopía UV-Vis

✅ ¡Éxito! Registrado Tecnico: Matías
✅ Experimento 'Espectroscopía UV-Vis' persistido con ID: 082aecab-46f7-427b-b990-48e0f8121269

==========================================
Selecciona una opción: 2

--- REGISTRAR ACCIÓN POLIMÓRFICA ---
1. Ejecutar tarea automática según el perfil de personal
2. Escribir descripción manual
Selecciona opción: 1
✅ Evento polimórfico registrado: 'Técnico Matías (Turno: Mañana) calibrando instrumental y preparando reactivos'

==========================================
Selecciona una opción: 3

Indica la nomenclatura de la nueva versión (ej. 'v1.1' o '2.0'): v2.0
✅ Experimento bifurcado y guardado. Nueva versión activa: v2.0

==========================================
Selecciona una opción: 4

--- ESTADO DEL EXPERIMENTO ---
ID:           9f1c3e20-8a11-4c9d-a012-77b1e4d90012
Nombre:       Espectroscopía UV-Vis
Versión:      v2.0
Responsable:  Matías (Instrumentación)
Estado:       En preparación

--- HISTORIAL DE TRAZABILIDAD ---
  [2026-11-26 17:15:10] (Usuario: 6614259d-f723-4bdf-b78d-42fc103c1a9f) -> Técnico Matías (Turno: Mañana) calibrando instrumental y preparando reactivos
  [2026-11-26 17:15:24] (Usuario: 6614259d-f723-4bdf-b78d-42fc103c1a9f) -> Bifurcación creada desde versión 1.0 -> v2.0

==========================================
Selecciona una opción: 6

Saliendo de LabTrack... ¡Hasta pronto!
```

### Escenario B: Interacción entre Dominio Rico, Servicio y Exportación de Informes
Demuestra cómo las entidades de `src/models/` protegen sus reglas de negocio mientras `LaboratorioService` coordina la persistencia y genera informes automáticos en Markdown:

```python
from src.services.laboratorio_service import LaboratorioService
from src.models.equipamiento import Equipamiento
from src.models.muestra import Muestra

# 1. Inicialización desacoplada mediante fábrica del servicio
servicio = LaboratorioService.crear_desde_sqlite("labtrack.db")

# 2. Alta de perfiles polimórficos y creación del experimento
investigador = servicio.registrar_personal("1", "Alonso", "Bioinformática", "Principal")
tecnico = servicio.registrar_personal("2", "Matías", "Instrumentación", "Mañana")
experimento = servicio.crear_experimento("Secuenciación Genómica", investigador)

# 3. Transiciones de estado y reglas de negocio del dominio
experimento.iniciar()  # 'En preparación' -> 'En curso'

espectrometro = Equipamiento("Espectrómetro UV", limite_usos_mantenimiento=1)
reactivo = Muestra("Reactivo ADN", cantidad=10.0, unidad="ml", umbral_critico=5.0)

experimento.utilizar_equipamiento(espectrometro)      # Agota usos -> pasa a 'En mantenimiento'
experimento.consumir_muestra(reactivo, cantidad=7.0)  # Stock restante: 3.0 ml -> alerta crítica

# 4. Control de autorización por rol e inmutabilidad post-cierre
try:
    experimento.finalizar(tecnico)  # Rechazado: solo un Investigador puede aprobar el cierre
except ValueError as err:
    print(f"Regla de negocio aplicada: {err}")

experimento.finalizar(investigador)  # Aceptado: estado -> 'Finalizado'
servicio.experimento_repo.guardar(experimento)
servicio.generar_informe_markdown("informe_secuenciacion.md")
servicio.cerrar()
```

### Escenario C: Trazabilidad Sincronizada en `labtrack.db` y `labtrack_system.log`
* **Registro de auditoría (`labtrack_system.log`):**
  ```text
  2026-11-26 17:15:02,110 - INFO - Iniciando aplicación LabTrack...
  2026-11-26 17:15:08,402 - INFO - Experimento creado y persistido: 082aecab-46f7-427b-b990-48e0f8121269
  2026-11-26 17:15:10,891 - INFO - Evento registrado en experimento 082aecab-46f7-427b-b990-48e0f8121269: Técnico Matías (Turno: Mañana) calibrando instrumental y preparando reactivos
  2026-11-26 17:15:24,310 - INFO - Experimento bifurcado a versión v2.0 (ID: 9f1c3e20-8a11-4c9d-a012-77b1e4d90012)
  2026-11-26 17:15:30,004 - INFO - Cierre limpio de la aplicación y liberación de recursos.
  ```
* **Filas persistidas en la tabla `trazabilidad` (`labtrack.db`):**
  ```text
  id_evento | id_experimento                       | accion
  ----------+--------------------------------------+---------------------------------------------------------------------------------
  1         | f47ac10b-58cc-4372-a567-0e02b2c3d479 | Inicio formal de ejecución experimental
  2         | f47ac10b-58cc-4372-a567-0e02b2c3d479 | Uso de equipamiento 'Espectrómetro UV' [ALERTA: Equipo enviado automáticamente a mantenimiento]
  3         | f47ac10b-58cc-4372-a567-0e02b2c3d479 | Consumo de 7.0 ml de 'Reactivo ADN' [ALERTA: Stock en nivel crítico]
  4         | f47ac10b-58cc-4372-a567-0e02b2c3d479 | Experimento finalizado y validado por Alonso
  ```

---

## 5. Arquitectura y Decisiones de Diseño (Guía del Desarrollador)

### Diagrama de Capas y Flujo de Dependencias

```text
+-------------------------------------------------------------------+
|                   CAPA DE PRESENTACIÓN (src/cli)                  |
|   main.py (Menú interactivo, modo --demo, captura de errores UI)  |
+---------------------------------+---------------------------------+
                                  | invoca casos de uso
                                  v
+-------------------------------------------------------------------+
|                  CAPA DE APLICACIÓN (src/services)                |
|   LaboratorioService (Orquestación, sesión, informes Markdown)    |
|   logger.py (Auditoría centralizada en labtrack_system.log)       |
+-----------------+---------------------------------+---------------+
                  | opera sobre                     | delega E/S
                  v                                 v
+---------------------------------+ +-------------------------------+
|    CAPA DE DOMINIO (src/models) | | CAPA PERSISTENCIA (persistence)|
| • Experimento (Agregado raíz)   | | • ConexionBaseDatos (SQLite)  |
| • Equipamiento (Desgaste/Estado)| | • PersonalRepository (SRP)    |
| • Muestra (Stock/Contaminación) | | • ExperimentoRepository (SRP) |
| • MiembroLaboratorio (ABC/Roles)| +-------------------------------+
| • EventoTrazabilidad (Inmutable)|
+---------------------------------+
```

### Decisiones Técnicas Clave
1. **Desacoplamiento estricto de la UI:** `src/cli/main.py` no importa `sqlite3` ni conoce los repositorios; recibe una instancia de `LaboratorioService` (Inyección de Dependencias), permitiendo sustituir la consola por una interfaz gráfica o web sin modificar la lógica de negocio.
2. **Modelo de Dominio Rico (sin entidades anémicas):**
   * `Experimento` impone su máquina de estados (`En preparación` $\rightarrow$ `En curso` $\rightarrow$ `Finalizado` / `Cancelado`) y bloquea mutaciones una vez cerrado.
   * `Equipamiento` contabiliza usos y transiciona automáticamente a `"En mantenimiento"` al alcanzar su límite operativo.
   * `Muestra` impide consumos o reposiciones si se marca como contaminada (`marcar_contaminada()`) y alerta al cruzar su umbral crítico.
   * `MiembroLaboratorio` (`Investigador` y `Tecnico`) encapsula políticas de autorización (`puede_aprobar_experimento()`, `puede_calibrar_equipo()`) y comportamiento polimórfico (`ejecutar_tarea()`).
   * `EventoTrazabilidad` sobrescribe `__setattr__` para garantizar inmutabilidad absoluta con marcas temporales UTC (`datetime.now(timezone.utc)`).
3. **Separación de Persistencia (SRP y Patrón Repositorio):** `ConexionBaseDatos` gestiona exclusivamente el ciclo de vida de SQLite con claves foráneas activas (`PRAGMA foreign_keys = ON`), mientras que `PersonalRepository` y `ExperimentoRepository` reconstruyen agregados completos desde disco (`obtener_por_id`), manteniendo intacto el polimorfismo de los responsables.
4. **Versionado Inmutable (`bifurcar_version`):** Utiliza `copy.deepcopy()` para clonar el agregado completo bajo un nuevo UUID y conservar la genealogía del historial.

---

## 6. Pruebas Automatizadas, Calidad y CI/CD

### Suite de Pruebas (`15 tests` / `88 % cobertura`)
Las pruebas se ejecutan con `pytest` y `pytest-cov`, superando el objetivo del 70 % e incluyendo pruebas unitarias, de integración con SQLite en memoria (`:memory:`), mocking de interfaz y flujos completos multisesión:

* `tests/test_main.py`: Validación de reglas básicas, casos límite de stock, bifurcación y polimorfismo.
* `tests/test_domain_rules.py`: Máquinas de estado de `Experimento` y `Equipamiento`, contaminación de `Muestra`, permisos por rol e inmutabilidad de eventos.
* `tests/test_database.py`: Integración con repositorios, reconstrucción polimórfica completa (`obtener_por_id`), búsquedas inexistentes e integridad referencial (`sqlite3.IntegrityError`).
* `tests/test_cli.py`: Simulación de sesión interactiva completa mediante `unittest.mock.patch` (opciones inválidas, errores de usuario controlados y salida limpia).
* `tests/test_e2e_workflows.py`: Prueba End-to-End entre dos sesiones independientes sobre archivo SQLite temporal (`tmp_path`), verificando persistencia, alertas y bloqueo post-cierre.

### Estilo, Linting e Integración Continua
* **PEP 8 y Análisis Estático:** El código cumple estrictamente con `black` (formateo) y `ruff` (linting) y utiliza anotaciones de tipo (*type hints*).
* **GitHub Actions (`.github/workflows/ci.yml`):** Cada `push` o `pull_request` a `main` ejecuta automáticamente `black --check`, `ruff check` y `pytest --cov=src --cov-fail-under=70`.

---

## 7. Estructura del Proyecto

```text
Trabajo-TCA-Gestor-de-Laboratorio/
├── .github/
│   └── workflows/
│       └── ci.yml                  # Pipeline CI (Black + Ruff + Pytest >= 70%)
├── docs/                           # Documentación API generada con pdoc
│   ├── index.html
│   └── ...
├── src/
│   ├── cli/
│   │   ├── __init__.py
│   │   └── main.py                 # Interfaz de consola y modo --demo
│   ├── models/
│   │   ├── __init__.py
│   │   ├── equipamiento.py         # Máquina de estados y desgaste de equipos
│   │   ├── experimento.py          # Agregado raíz, ciclo de vida y bifurcación
│   │   ├── muestra.py              # Control de stock, contaminación y alertas
│   │   ├── personal.py             # Jerarquía ABC (Investigador / Técnico)
│   │   └── trazabilidad.py         # Eventos inmutables con timestamp UTC
│   ├── persistence/
│   │   ├── __init__.py
│   │   ├── database.py             # Conexión SQLite y esquema relacional
│   │   └── repositories.py         # PersonalRepository y ExperimentoRepository
│   └── services/
│       ├── __init__.py
│       ├── laboratorio_service.py  # Capa de aplicación, sesión e informes MD
│       └── logger.py               # Configuración centralizada de logging
├── tests/
│   ├── test_cli.py                 # Pruebas de flujo CLI con mocking
│   ├── test_database.py            # Pruebas de integración y repositorios
│   ├── test_domain_rules.py        # Pruebas de invariantes y máquinas de estado
│   ├── test_e2e_workflows.py       # Pruebas End-to-End multisesión
│   └── test_main.py                # Pruebas unitarias núcleo y casos límite
├── .env.example                    # Plantilla de variables de entorno
├── .gitignore                      # Exclusión de venv, __pycache__, *.db y *.log
├── CHANGELOG.md                    # Historial de versiones (v0.1.0 -> v1.0.0)
├── LICENSE                         # Licencia MIT
├── pyproject.toml                  # Empaquetado PEP 621 y configuración de herramientas
└── README.md                       # Documentación principal del proyecto
```

---

## 8. Roadmap Breve

* **`v0.1.0` (PRAC2):** Diseño inicial Orientado a Objetos, jerarquía de personal, trazabilidad en memoria y bifurcación inmutable de versiones.
* **`v0.2.0` (PRAC3):** Persistencia relacional en SQLite, logging centralizado (`labtrack_system.log`), manejo de excepciones y primeras pruebas con `pytest`.
* **`v1.0.0` (PRAC4 — Actual):** Arquitectura desacoplada en 4 capas, repositorios independientes (SRP), dominio rico con máquinas de estado, exportación automática de informes en Markdown, modo `--demo`, pipeline CI/CD y cobertura del **88 %**.
* **`v1.1.0` (Futuro):** Incorporación de una interfaz web (FastAPI / Streamlit) conectada directamente a `LaboratorioService` y exportación de informes en PDF.

---

## 9. Registro de Contribuciones

| Integrante | Rol y Responsabilidades Principales |
| :--- | :--- |
| **Alonso Villalba Pintado** | Arquitectura en capas, capa de persistencia (`database.py`, `repositories.py`), `LaboratorioService`, empaquetado PEP 621, configuración CI/CD y suite de pruebas (`pytest`, integración y E2E). |
| **Matías Mayor** | Modelado del dominio (`Experimento`, `Equipamiento`, `Muestra`, `Personal`), implementación de máquinas de estado, invariantes de negocio y trazabilidad inmutable. |
| **Antonio Hermana Rubio** | Interfaz de consola (`main.py`), modo `--demo`, sistema de logging, generación automática de informes en Markdown, documentación técnica (`README.md`, `pdoc`) y casos de prueba. |

---

## 10. Atribuciones (Uso de IA) y Licencia

### Atribuciones y Uso de Herramientas de IA
En cumplimiento de la política académica de la asignatura *Técnicas de Programación Avanzada*, se declara el uso de **Google Gemini** como asistente de apoyo durante el desarrollo para:
* Revisión arquitectónica y refactorización hacia una separación estricta de capas (aplicación del Principio de Responsabilidad Única en repositorios y desacoplamiento de la CLI).
* Diseño de casos de prueba límite, de integración con SQLite y de flujos End-to-End.
* Estructuración de la documentación técnica y configuración de herramientas de calidad (`pyproject.toml`, `black`, `ruff`, GitHub Actions).

Todo el código generado o sugerido ha sido revisado, adaptado, probado y validado íntegramente por los miembros del Grupo 2, quienes asumen la plena responsabilidad sobre su funcionamiento, estructura y resultados.

### Licencia
Este proyecto se distribuye bajo los términos de la **Licencia MIT**. Consulta el archivo [`LICENSE`](LICENSE) para más detalles.