# LabTrack 🔬

Gestor integral para laboratorios de investigación. Permite controlar experimentos, muestras, equipamiento y garantizar la trazabilidad completa de los resultados.

## Estructura del Proyecto (Arquitectura)
Para mantener un código limpio y escalable, el proyecto se divide en las siguientes capas:
- `src/models/`: Entidades principales del dominio (Investigador, Muestra, Equipamiento, Experimento) y lógica central de Trazabilidad.
- `src/services/`: Lógica de negocio, controladores y generación de informes automáticos.
- `src/persistence/`: Módulos preparados para la futura persistencia e integración con bases de datos (SQLite).
- `src/cli/`: Interfaz de línea de comandos (punto de entrada de la aplicación).
- `tests/`: Batería de pruebas automatizadas configurada con `pytest`.

## Requisitos
- **Python 3.9** o superior.
- **Git** (para el control de versiones).

## Instalación y Configuración del Entorno

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/alonsovillalbapintado/Trabajo-TCA-Gestor-de-Laboratorio.git
   cd Trabajo-TCA-Gestor-de-Laboratorio

## Crear el entorno virtual:

python -m venv venv

## Activar el entorno virtual:

- `En Windows (PowerShell)`:

PowerShell

venv\Scripts\activate

- `En Linux/macOS`:

source venv/bin/activate

## Instalar las dependencias de desarrollo:

pip install -e .[dev]

## Ejecución

Para iniciar la aplicación y acceder al menú interactivo principal, ejecuta el siguiente comando con el entorno virtual activado:

python -m src.cli.main

## Pruebas

El proyecto cuenta con un sistema de pruebas automatizadas. Para lanzar la batería de pruebas (Smoke Tests y Unitarias):

pytest tests/

## Roadmap y Próximos Pasos
PRAC2 (Actual): Desarrollo de las clases de dominio, implementación del sistema de eventos de trazabilidad, lógica de versionado (bifurcación) de experimentos y pruebas unitarias (cobertura > 35%).

PRAC3: Implementación de persistencia de datos mediante SQLite para el almacenamiento permanente del historial y entidades.

## Atribuciones

Esta sección se mantendrá actualizada durante el ciclo de vida del proyecto para detallar el uso de asistentes de Inteligencia Artificial (ChatGPT, Gemini, Claude, etc.) o fragmentos de código de terceros, cumpliendo estrictamente con la política de transparencia académica de la asignatura.