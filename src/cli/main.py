import sys
from src.models.personal import Investigador, Tecnico
from src.models.experimento import Experimento
from src.models.muestra import Muestra
from src.models.equipamiento import Equipamiento

# Añade esta importación arriba con las demás
from src.persistence.database import GestorBaseDatos

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
    # 1. Arrancamos la conexión a la base de datos
    db = GestorBaseDatos()
    
    # Variables para mantener los objetos en memoria durante la ejecución
    experimento_actual = None
    investigador_actual = None

    while True:
        opcion = mostrar_menu()

        if opcion == '1':
            print("\n--- ALTA DE PERSONAL Y EXPERIMENTO ---")
            tipo_personal = input("¿Qué desea registrar? (1: Investigador / 2: Técnico): ").strip()
            nombre = input("Nombre: ")
            especialidad = input("Especialidad/Área: ")
            
            if tipo_personal == '2':
                turno = input("Turno (Mañana/Tarde/Noche): ")
                # Instanciamos la subclase Tecnico
                investigador_actual = Tecnico(nombre, especialidad, turno)
            else:
                rol = input("Rol (Principal/Asistente): ") or "Principal"
                # Instanciamos la subclase Investigador
                investigador_actual = Investigador(nombre, especialidad, rol)
            
            print("\n--- NUEVO EXPERIMENTO ---")
            nombre_exp = input("Nombre del experimento: ")
            experimento_actual = Experimento(nombre_exp, investigador_actual)
            
            # NUEVO: Guardamos el experimento recién creado en SQLite
            db.guardar_experimento(experimento_actual)
            
            print(f"\n✅ ¡Éxito! Registrado {investigador_actual.__class__.__name__}: {investigador_actual.nombre}")
            print(f"✅ Experimento '{experimento_actual.nombre}' creado con ID: {experimento_actual.id_experimento}")

        elif opcion == '2':
            if not experimento_actual:
                print("\n❌ Error: Primero debes crear un experimento (Opción 1).")
                continue
            
            print("\n--- REGISTRAR ACCIÓN POLIMÓRFICA ---")
            print("1. Ejecutar tarea automática según el perfil de personal")
            print("2. Escribir descripción manual")
            sub_op = input("Selecciona opción: ").strip()

            if sub_op == '1':
                # Llamada al método polimórfico conectado a la trazabilidad
                accion = experimento_actual.asignar_y_ejecutar_tarea(investigador_actual)
                print(f"✅ Evento polimórfico registrado: '{accion}'")
            else:
                accion = input("Describe la acción realizada: ")
                experimento_actual.registrar_evento(accion)
                
            # NUEVO: Actualizamos el experimento en SQLite para que guarde el nuevo evento
            db.guardar_experimento(experimento_actual)
            print("✅ Evento registrado en el historial y guardado en Base de Datos.")

        elif opcion == '3':
            if not experimento_actual:
                print("\n❌ Error: No hay ningún experimento activo.")
                continue
            
            nueva_version = input("\nIndica la nomenclatura de la nueva versión (ej. 'v1.1' o '2.0'): ")
            # Llamamos al método real que hace la copia profunda
            experimento_actual = experimento_actual.bifurcar_version(nueva_version)
            
            # NUEVO: Guardamos la nueva versión bifurcada (se creará una fila nueva en SQLite por tener otro UUID)
            db.guardar_experimento(experimento_actual)
            print(f"✅ Experimento bifurcado y guardado en Base de Datos. Nueva versión activa: {experimento_actual.version}")

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
                    # Al imprimir el objeto 'evento', Python usa automáticamente su método __str__
                    print(f"  {evento}")

        elif opcion == '5':
            print("\nSaliendo de LabTrack... ¡Hasta pronto!")
            sys.exit(0)
        
        else:
            print("\n❌ Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    ejecutar_flujo_principal()