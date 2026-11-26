# Changelog

Todos los cambios notables de **LabTrack** se documentan en este archivo.

## [1.0.0] - 2026-11-26

### Añadido (Entrega Final - PRAC4)
- **Capa de Aplicación (`LaboratorioService`):** Orquestación centralizada de casos de uso, fábrica de infraestructura SQLite y gestión del estado de sesión activo.
- **Repositorios Independientes (`PersonalRepository` y `ExperimentoRepository`):** Separación del acceso a datos por agregado aplicando el Principio de Responsabilidad Única (SRP) y reconstrucción polimórfica desde base de datos (`obtener_por_id`).
- **Modo Demo (`--demo`) e Informes Automáticos:** Ejecución desatendida para validación rápida en clase y exportación de informes técnicos en formato Markdown.
- **Reglas de Negocio en Dominio:** Máquinas de estado en `Experimento` y `Equipamiento` (paso automático a mantenimiento por desgaste), control de contaminación y umbral crítico en `Muestra`, políticas de autorización por rol en `MiembroLaboratorio` e inmutabilidad estricta en `EventoTrazabilidad`.
- **Suite de Pruebas Ampliada (87 % cobertura):** Incorporación de `test_domain_rules.py` y `test_e2e_workflows.py` para validar recuperación multisesión, integridad referencial y errores de usuario.
- **Calidad, CI/CD y Documentación:** Pipeline en GitHub Actions (`black`, `ruff`, `pytest`), licencia MIT, `.env.example` y documentación API en `docs/`.

### Cambiado
- **Empaquetado PEP 621 (`pyproject.toml`):** Separación de dependencias de ejecución (`dependencies = []`) y herramientas de desarrollo (`[project.optional-dependencies] dev`).
- **Desacoplamiento de Interfaz (`src/cli/main.py`):** Eliminación de referencias directas a SQLite y repositorios en la capa de presentación.

## [0.2.0] - 2026-11-15
### Añadido (PRAC3)
- Persistencia relacional con SQLite (`labtrack.db`) y soporte de bases de datos volátiles (`:memory:`) para pruebas.
- Sistema de logging centralizado en `labtrack_system.log` (`INFO`, `WARNING`, `ERROR`).
- Manejo robusto de excepciones en la interfaz de consola y tests iniciales con `pytest` y `unittest.mock`.

## [0.1.0] - 2026-10-30
### Añadido (PRAC2)
- Modelo inicial Orientado a Objetos (`Experimento`, `Muestra`, `Equipamiento`, `Investigador`, `Tecnico`, `EventoTrazabilidad`).
- Motor de trazabilidad con marcas temporales y bifurcación inmutable de versiones (`copy.deepcopy`).