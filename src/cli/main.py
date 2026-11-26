import sys
from src.persistence.database import ConexionBaseDatos
from src.persistence.repositories import PersonalRepository, ExperimentoRepository
from src.services.laboratorio_service import LaboratorioService
from src.services.logger import get_logger

def mostrar_menu():
    print("\n" + "=" * 40)
    print("🔬 LABTRACK: GESTOR DE LABORATORIO 🔬")
    print("=" * 40)
    print("1. Crear nuevo Personal y Experimento")
    print("2. Registrar evento de Trazabilidad")
    print("3. Bifurcar Experimento (Crear nueva versión)")
    print("4. Mostrar estado actual y Trazabilidad")
    print("5. Salir")
    print("=" * 40)
    return input("Selecciona una opción: ").strip()

def ejecutar_flujo_principal():
    logger = get_logger()
    logger.info("Iniciando aplicación LabTrack...")

    try:
        db = ConexionBaseDatos()
        personal_repo = PersonalRepository(db.conexion)
        experimento_repo = ExperimentoRepository(db.conexion, personal_repo)
        servicio = LaboratorioService(experimento_repo)
        logger.info("Capas de persistencia y servicio inicializadas con éxito.")
    except Exception as e:
        print(f"\n❌ Error fatal al inicializar el sistema: {e}")
        logger.error(f"Fallo de inicialización: {e}")
        sys.exit(1)

    experimento_actual = None
    investigador_actual = None

    while True:
        opcion = mostrar_menu()

        if opcion == "1":
            print("\n--- ALTA DE PERSONAL Y EXPERIMENTO ---")
            try:
                tipo_personal = input("¿Qué desea registrar? (1: Investigador / 2: Técnico): ").strip()
                nombre = input("Nombre: ")
                especialidad = input("Especialidad/Área: ")
                detalle = input("Turno (Mañana/Tarde/Noche): ") if tipo_personal == "2" else input("Rol (Principal/Asistente): ")

                investigador_actual = servicio.registrar_personal(tipo_personal, nombre, especialidad, detalle)

                print("\n--- NUEVO EXPERIMENTO ---")
                nombre_exp = input("Nombre del experimento: ")
                experimento_actual = servicio.crear_experimento(nombre_exp, investigador_actual)

                print(f"\n✅ ¡Éxito! Registrado {investigador_actual.__class__.__name__}: {investigador_actual.nombre}")
                print(f"✅ Experimento '{experimento_actual.nombre}' persistido con ID: {experimento_actual.id_experimento}")

            except Exception as e:
                print("\n❌ Ocurrió un error al crear los registros. Por favor, inténtalo de nuevo.")
                logger.error(f"Error en Opción 1 (Creación): {e}")

        elif opcion == "2":
            if not experimento_actual:
                print("\n❌ Error: Primero debes crear un experimento (Opción 1).")
                continue

            print("\n--- REGISTRAR ACCIÓN POLIMÓRFICA ---")
            print("1. Ejecutar tarea automática según el perfil de personal")
            print("2. Escribir descripción manual")
            sub_op = input("Selecciona opción: ").strip()

            try:
                if sub_op == "1":
                    accion = servicio.registrar_evento(experimento_actual, investigador_actual, automatico=True)
                    print(f"✅ Evento polimórfico registrado: '{accion}'")
                else:
                    desc = input("Describe la acción realizada: ")
                    servicio.registrar_evento(experimento_actual, investigador_actual, automatico=False, descripcion=desc)
                    print("✅ Evento guardado correctamente.")

            except ValueError as e:
                print(f"\n❌ Acción denegada por regla de negocio: {e}")
                logger.warning(f"Intento de acción denegado: {e}")
            except Exception as e:
                print("\n❌ Ha ocurrido un error inesperado al registrar el evento.")
                logger.error(f"Error inesperado en Opción 2: {e}")

        elif opcion == "3":
            if not experimento_actual:
                print("\n❌ Error: No hay ningún experimento activo.")
                continue

            try:
                nueva_version = input("\nIndica la nomenclatura de la nueva versión (ej. 'v1.1' o '2.0'): ")
                experimento_actual = servicio.bifurcar_experimento(experimento_actual, nueva_version)
                print(f"✅ Experimento bifurcado y guardado. Nueva versión activa: {experimento_actual.version}")

            except Exception as e:
                print("\n❌ Ocurrió un error al bifurcar el experimento.")
                logger.error(f"Error en Opción 3 (Bifurcar): {e}")

        elif opcion == "4":
            if not experimento_actual:
                print("\n❌ Error: No hay ningún experimento activo.")
                continue

            print("\n--- ESTADO DEL EXPERIMENTO ---")
            print(f"Nombre:       {experimento_actual.nombre}")
            print(f"Versión:      {experimento_actual.version}")
            print(f"Responsable:  {experimento_actual.investigador_principal.nombre} ({experimento_actual.investigador_principal.especialidad})")
            print(f"Estado:       {experimento_actual.estado}")

            print("\n--- HISTORIAL DE TRAZABILIDAD ---")
            if not experimento_actual.historial_eventos:
                print("  (Sin eventos registrados)")
            else:
                for evento in experimento_actual.historial_eventos:
                    print(f"  {evento}")

        elif opcion == "5":
            print("\nSaliendo de LabTrack... ¡Hasta pronto!")
            db.cerrar()
            logger.info("Cierre limpio de la aplicación por el usuario.")
            sys.exit(0)

        else:
            print("\n❌ Opción no válida. Inténtalo de nuevo.")
            logger.warning(f"El usuario intentó usar una opción inválida: {opcion}")

if __name__ == "__main__":
    ejecutar_flujo_principal()