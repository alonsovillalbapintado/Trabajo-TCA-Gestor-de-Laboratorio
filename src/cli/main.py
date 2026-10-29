def mostrar_menu_principal():
    """Muestra el menú principal de LabTrack."""
    print("=" * 40)
    print("🔬 Bienvenido a LabTrack v0.1 🔬")
    print("=" * 40)
    print("1. Registrar nuevo experimento")
    print("2. Consultar muestras")
    print("3. Generar informe de trazabilidad")
    print("4. Salir")
    print("-" * 40)

def procesar_opcion(opcion):
    """Procesa la opción seleccionada simulando un flujo."""
    if opcion == "1":
        return "Abriendo módulo de creación de experimentos..."
    elif opcion == "2":
        return "Cargando inventario de muestras..."
    elif opcion == "3":
        return "Generando informe automático..."
    elif opcion == "4":
        return "Saliendo del sistema..."
    else:
        return "Opción no válida. Intente de nuevo."

def main():
    mostrar_menu_principal()
    # Simulación de entrada para la Prueba de Concepto (PoC)
    print("Simulando entrada del usuario: Opción 1")
    resultado = procesar_opcion("1")
    print(f">> {resultado}")

if __name__ == "__main__":
    main()