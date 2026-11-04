# 🔬 LabTrack - Gestor de Laboratorio de Investigación

**Grupo 2**  
**Integrantes:** Matías Mayor, Alonso Villalba Pintado, Antonio Hermana Rubio  
**Asignatura:** Técnicas de Programación Avanzada (PRAC2)  

LabTrack es un sistema de gestión de laboratorios diseñado con una arquitectura robusta Orientada a Objetos (POO). Su objetivo es garantizar la trazabilidad inmutable de los experimentos y gestionar los recursos (personal, muestras y equipamiento) del laboratorio.

---

## 1. Arquitectura Orientada a Objetos (El Dominio)

El sistema se divide en capas (`cli/`, `models/`, `services/`, `persistence/`, `tests/`) para separar la lógica de negocio de la interfaz. En la capa de modelos (`src/models/`), interactúan las siguientes entidades principales:

* **`Experimento`**: Clase central que asocia un responsable, recursos y un historial de eventos.
* **`Muestra`**: Gestiona el stock físico. Lanza excepciones (`ValueError`) si se intenta consumir más cantidad de la disponible.
* **`Equipamiento`**: Maquinaria con estados controlados ("Disponible", "En mantenimiento").
* **`EventoTrazabilidad`**: Entidad inmutable que captura el "cuándo" (`datetime.now()`), "quién" y "qué" de cada acción.

---

## 2. Herencia y Polimorfismo (Núcleo PRAC2)

Para modelar al equipo de trabajo, hemos implementado una jerarquía de clases que demuestra el uso práctico de **herencia y polimorfismo**:

* **Superclase Abstracta:** `MiembroLaboratorio`. Define los atributos comunes (`id_miembro` mediante `uuid4`, `nombre`, `especialidad`) y un método abstracto `@abstractmethod def ejecutar_tarea()`.
* **Subclases (Herencia):** Las clases `Investigador` y `Tecnico` heredan de `MiembroLaboratorio` y sobrescriben el método `ejecutar_tarea()` con comportamientos distintos.
* **Polimorfismo en Acción:** La clase `Experimento` posee el método `asignar_y_ejecutar_tarea(miembro: MiembroLaboratorio)`. Este método recibe un objeto genérico y ejecuta su tarea automáticamente, demostrando un acoplamiento débil y polimorfismo puro.

---

## 3. Motor de Trazabilidad y Versionado

La **trazabilidad** es el pilar de LabTrack. No guardamos simples textos, sino que:
1. Cada acción instancia un objeto `EventoTrazabilidad`.
2. Se almacena en la lista `historial_eventos` de la clase `Experimento`.
3. Todo queda ligado al ID único (`uuid4`) del investigador que realizó la acción.

**Versionado:** Para evitar que un experimento se convierta en un simple CRUD, hemos implementado el método `bifurcar_version(nueva_version)`. Mediante `copy.deepcopy()`, clona el experimento entero, generando un nuevo `id_experimento` pero preservando de forma idéntica el historial de trazabilidad anterior.

---

## 4. Ejemplos de Uso (Flujo de Consola CLI)

El programa se ejecuta interactuando con la terminal (`python -m src.cli.main`). A continuación, un ejemplo real de ejecución:

```text
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
✅ Experimento 'Calibración A1' creado con ID: f82d1c9a-3b21-4f1e...tica de transparencia académica de la asignatura.

5. Pruebas Automatizadas y Cobertura (Testing)
Se ha desarrollado una batería de pruebas con pytest en tests/test_main.py evaluando:

Pruebas de Herencia y Polimorfismo.

Casos límite (ej. consumir el 100% exacto de una muestra).

Entradas inválidas y Excepciones (ej. rechazar consumos de muestra negativos o superiores al stock lanzando ValueError).

Escenarios alternativos y trazabilidad (ej. bifurcar experimentos vacíos).

Resultados de la Ejecución de Pruebas:

Comando ejecutado: python -m pytest --cov=src tests/

Tests pasados: 6 / 6 exitosos.

Cobertura (Coverage): El núcleo de lógica de negocio (capa models/) mantiene una cobertura del 98.5%, demostrando una alta fiabilidad en las entidades de dominio antes de afrontar la persistencia.

6. Siguiente fase: Persistencia (PRAC3)
El sistema ya está preparado para la PRAC3. Todas las entidades utilizan uuid.uuid4() para generar identificadores únicos universales, lo que garantiza una transición natural hacia claves primarias (Primary Keys) cuando integremos la base de datos SQLite en el módulo src/persistence/.