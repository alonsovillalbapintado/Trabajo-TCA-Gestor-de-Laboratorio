import sys
from src.models.investigador import Investigador
from src.models.experimento import Experimento
from src.models.muestra import Muestra
from src.models.equipamiento import Equipamiento

def mostrar_menu():
    print("\n" + "="*40)
    print("🔬 LABTRACK: GESTOR DE LABORATORIO 🔬")
    print("="*40)
    print("1. Crear nuevo Investigador y Experimento")
    print("2. Registrar evento de Trazabilidad")
    print("3. Bifurcar Experimento (Crear nueva versión)")
    print("4. Mostrar estado actual y Trazabilidad")
    print("5. Salir")
    print("="*40)
    return input("Selecciona una opción: ").strip()

def ejecutar_flujo_principal():
    # Variables para mantener los objetos en memoria durante la ejecución
    experimento_actual = None
    investigador_actual = None

    while True:
        opcion = mostrar_menu()

        if opcion == '1':
            print("\n--- ALTA DE INVESTIGADOR ---")
            nombre_inv = input("Nombre del investigador: ")
            especialidad = input("Especialidad: ")
            # Instanciamos un objeto Investigador real
            investigador_actual = Investigador(nombre_inv, especialidad, "Investigador Principal")
            
            print("\n--- NUEVO EXPERIMENTO ---")
            nombre_exp = input("Nombre del experimento: ")
            # Instanciamos un objeto Experimento pasándole el investigador
            experimento_actual = Experimento(nombre_exp, investigador_actual)
            
            print(f"\n✅ ¡Éxito! Experimento '{experimento_actual.nombre}' creado.")
            print(f"   ID interno: {experimento_actual.id_experimento}")

        elif opcion == '2':
            if not experimento_actual:
                print("\n❌ Error: Primero debes crear un experimento (Opción 1).")
                continue
            
            accion = input("\nDescribe la acción realizada (ej. 'Muestra centrifugada a 3000 rpm'): ")
            # Llamamos al método real que añade un EventoTrazabilidad al historial
            experimento_actual.registrar_evento(accion)
            print("✅ Evento registrado en el historial de trazabilidad.")

        elif opcion == '3':
            if not experimento_actual:
                print("\n❌ Error: No hay ningún experimento activo.")
                continue
            
            nueva_version = input("\nIndica la nomenclatura de la nueva versión (ej. 'v1.1' o '2.0'): ")
            # Llamamos al método real que hace la copia profunda
            experimento_actual = experimento_actual.bifurcar_version(nueva_version)
            print(f"✅ Experimento bifurcado correctamente. Nueva versión activa: {experimento_actual.version}")

        elif opcion == '4':
            if not experimento_actual:
                print("\n❌ Error: No hay ningún experimento activo.")
                continue
            
            print(f"\n--- ESTADO DEL EXPERIMENTO ---")
            print(f"Nombre:       {experimento_actual.nombre}")
            print(f"Versión:      {experimento_actual.version}")
            print(f"Investigador: {experimento_actual.investigador_principal.nombre} ({experimento_actual.investigador_principal.especialidad})")
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