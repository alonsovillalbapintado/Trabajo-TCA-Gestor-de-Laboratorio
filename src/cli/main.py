import sys
from src.models.personal import Investigador, Tecnico
from src.models.experimento import Experimento
from src.models.muestra import Muestra
from src.models.equipamiento import Equipamiento

from src.persistence.database import GestorBaseDatos
from src.services.logger import get_logger

def mostrar_menu():
    print("\n" + "="*40)
    print("🔬 LABTRACK: GESTOR DE LABORATORIO 🔬")
    print("="*40)
    print("1. Crear nuevo Personal y Experimento") 
    print("2. Registrar evento de Trazabilidad")
    print("3. Bifurcar Experimento (Crear nueva versión)")
    print("4. Mostrar estado actual y Trazabilidad")
    print("5. Salir")
    print("="*40)
    return input("Selecciona una opción: ").strip()

def ejecutar_flujo_principal():
    # 1. Arrancamos el Logger
    logger = get_logger()
    logger.info("Iniciando aplicación LabTrack...")

    # 2. Conectamos a SQLite protegidos por un bloque try/except
    try:
        db = GestorBaseDatos()
        logger.info("Conexión a base de datos inicializada con éxito.")
    except Exception as e:
        print(f"\n❌ Error fatal al conectar con la base de datos. Detalles: {e}")
        logger.error(f"Fallo de persistencia al arrancar: {e}")
        sys.exit(1) # Cerramos el programa porque sin BD no podemos funcionar
    
    experimento_actual = None
    investigador_actual = None

    while True:
        opcion = mostrar_menu()

        if opcion == '1':
            print("\n--- ALTA DE PERSONAL Y EXPERIMENTO ---")
            try:
                tipo_personal = input("¿Qué desea registrar? (1: Investigador / 2: Técnico): ").strip()
                nombre = input("Nombre: ")
                especialidad = input("Especialidad/Área: ")
                
                if tipo_personal == '2':
                    turno = input("Turno (Mañana/Tarde/Noche): ")
                    investigador_actual = Tecnico(nombre, especialidad, turno)
                else:
                    rol = input("Rol (Principal/Asistente): ") or "Principal"
                    investigador_actual = Investigador(nombre, especialidad, rol)
                
                print("\n--- NUEVO EXPERIMENTO ---")
                nombre_exp = input("Nombre del experimento: ")
                experimento_actual = Experimento(nombre_exp, investigador_actual)
                
                # Intentamos guardar en la BD
                db.guardar_experimento(experimento_actual)
                
                print(f"\n✅ ¡Éxito! Registrado {investigador_actual.__class__.__name__}: {investigador_actual.nombre}")
                print(f"✅ Experimento '{experimento_actual.nombre}' persistido con ID: {experimento_actual.id_experimento}")
                
                logger.info(f"Nuevo experimento creado y guardado: {experimento_actual.id_experimento}")
            
            except Exception as e:
                print(f"\n❌ Ocurrió un error al crear los registros. Por favor, inténtalo de nuevo.")
                logger.error(f"Error en Opción 1 (Creación): {e}")

        elif opcion == '2':
            if not experimento_actual:
                print("\n❌ Error: Primero debes crear un experimento (Opción 1).")
                continue
            
            print("\n--- REGISTRAR ACCIÓN POLIMÓRFICA ---")
            print("1. Ejecutar tarea automática según el perfil de personal")
            print("2. Escribir descripción manual")
            sub_op = input("Selecciona opción: ").strip()

            try:
                if sub_op == '1':
                    accion = experimento_actual.asignar_y_ejecutar_tarea(investigador_actual)
                    print(f"✅ Evento polimórfico registrado: '{accion}'")
                else:
                    accion = input("Describe la acción realizada: ")
                    experimento_actual.registrar_evento(accion)
                    
                # Guardamos la actualización en la BD
                db.guardar_experimento(experimento_actual)
                print("✅ Evento guardado correctamente en la Base de Datos.")
                logger.info("Nuevo evento de trazabilidad persistido en SQLite.")
                
            except ValueError as e:
                # Si tienes reglas de negocio (ej. falta de muestra), saltará aquí
                print(f"\n❌ Acción denegada por regla de negocio: {e}")
                logger.warning(f"Intento de acción denegado: {e}")
            except Exception as e:
                print("\n❌ Ha ocurrido un error inesperado al registrar el evento.")
                logger.error(f"Error inesperado en Opción 2: {e}")

        elif opcion == '3':
            if not experimento_actual:
                print("\n❌ Error: No hay ningún experimento activo.")
                continue
            
            try:
                nueva_version = input("\nIndica la nomenclatura de la nueva versión (ej. 'v1.1' o '2.0'): ")
                experimento_actual = experimento_actual.bifurcar_version(nueva_version)
                
                db.guardar_experimento(experimento_actual)
                print(f"✅ Experimento bifurcado y guardado en Base de Datos. Nueva versión activa: {experimento_actual.version}")
                logger.info(f"Experimento bifurcado a la versión {nueva_version} y persistido.")
                
            except Exception as e:
                print("\n❌ Ocurrió un error al bifurcar el experimento.")
                logger.error(f"Error en Opción 3 (Bifurcar): {e}")

        elif opcion == '4':
            if not experimento_actual:
                print("\n❌ Error: No hay ningún experimento activo.")
                continue
            
            print(f"\n--- ESTADO DEL EXPERIMENTO ---")
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

        elif opcion == '5':
            print("\nSaliendo de LabTrack... ¡Hasta pronto!")
            logger.info("Cierre limpio de la aplicación por el usuario.")
            sys.exit(0)
        
        else:
            print("\n❌ Opción no válida. Inténtalo de nuevo.")
            logger.warning(f"El usuario intentó usar una opción inválida: {opcion}")

if __name__ == "__main__":
    ejecutar_flujo_principal()