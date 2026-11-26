import sys

from src.services.laboratorio_service import LaboratorioService
from src.services.logger import get_logger


def mostrar_menu():
    print("\n" + "=" * 42)
    print("🔬 LABTRACK: GESTOR DE LABORATORIO 🔬")
    print("=" * 42)
    print("1. Crear nuevo Personal y Experimento")
    print("2. Registrar evento de Trazabilidad")
    print("3. Bifurcar Experimento (Crear nueva versión)")
    print("4. Mostrar estado actual y Trazabilidad")
    print("5. Recuperar Experimento existente por ID")
    print("6. Salir")
    print("=" * 42)
    return input("Selecciona una opción: ").strip()


def ejecutar_flujo_principal(servicio: LaboratorioService | None = None):
    logger = get_logger()
    logger.info("Iniciando aplicación LabTrack...")

    try:
        servicio = servicio or LaboratorioService.crear_desde_sqlite()
    except Exception as e:  # noqa: BLE001
        print(f"\n❌ Error fatal al inicializar el sistema: {e}")
        logger.error(f"Fallo de inicialización: {e}")
        sys.exit(1)

    while True:
        opcion = mostrar_menu()

        if opcion == "1":
            print("\n--- ALTA DE PERSONAL Y EXPERIMENTO ---")
            try:
                tipo_personal = input(
                    "¿Qué desea registrar? (1: Investigador / 2: Técnico): "
                ).strip()
                nombre = input("Nombre: ")
                especialidad = input("Especialidad/Área: ")
                detalle = (
                    input("Turno (Mañana/Tarde/Noche): ")
                    if tipo_personal == "2"
                    else input("Rol (Principal/Asistente): ")
                )
                nombre_exp = input("Nombre del experimento: ")

                resumen = servicio.iniciar_nueva_sesion(
                    tipo_personal, nombre, especialidad, detalle, nombre_exp
                )
                print(
                    f"\n✅ ¡Éxito! Registrado {resumen['perfil']}: {resumen['responsable']}"
                )
                print(
                    f"✅ Experimento '{resumen['experimento']}' persistido con ID: {resumen['id_experimento']}"
                )

            except ValueError as e:
                print(f"\n❌ Datos no válidos: {e}")
                logger.warning(f"Validación fallida en alta: {e}")
            except Exception as e:  # noqa: BLE001
                print("\n❌ Ocurrió un error inesperado al crear los registros.")
                logger.error(f"Error en Opción 1: {e}")

        elif opcion == "2":
            print("\n--- REGISTRAR ACCIÓN POLIMÓRFICA ---")
            print("1. Ejecutar tarea automática según el perfil de personal")
            print("2. Escribir descripción manual")
            sub_op = input("Selecciona opción: ").strip()

            try:
                if sub_op == "1":
                    accion = servicio.registrar_evento_activo(automatico=True)
                    print(f"✅ Evento polimórfico registrado: '{accion}'")
                else:
                    desc = input("Describe la acción realizada: ")
                    servicio.registrar_evento_activo(automatico=False, descripcion=desc)
                    print("✅ Evento guardado correctamente.")

            except ValueError as e:
                print(f"\n❌ Acción denegada: {e}")
                logger.warning(f"Acción denegada en Opción 2: {e}")
            except Exception as e:  # noqa: BLE001
                print("\n❌ Error inesperado al registrar el evento.")
                logger.error(f"Error en Opción 2: {e}")

        elif opcion == "3":
            try:
                nueva_version = input(
                    "\nIndica la nomenclatura de la nueva versión (ej. 'v1.1' o '2.0'): "
                )
                bifurcado = servicio.bifurcar_experimento_activo(nueva_version)
                print(
                    f"✅ Experimento bifurcado y guardado. Nueva versión activa: {bifurcado.version}"
                )

            except ValueError as e:
                print(f"\n❌ No se pudo bifurcar: {e}")
                logger.warning(f"Validación en Opción 3: {e}")
            except Exception as e:  # noqa: BLE001
                print("\n❌ Error inesperado al bifurcar el experimento.")
                logger.error(f"Error en Opción 3: {e}")

        elif opcion == "4":
            try:
                datos = servicio.obtener_resumen_sesion()
                print("\n--- ESTADO DEL EXPERIMENTO ---")
                print(f"ID:           {datos['id']}")
                print(f"Nombre:       {datos['nombre']}")
                print(f"Versión:      {datos['version']}")
                print(f"Responsable:  {datos['responsable']}")
                print(f"Estado:       {datos['estado']}")

                print("\n--- HISTORIAL DE TRAZABILIDAD ---")
                if not datos["eventos"]:
                    print("  (Sin eventos registrados)")
                else:
                    for evento in datos["eventos"]:
                        print(f"  {evento}")
            except ValueError as e:
                print(f"\n❌ {e}")

        elif opcion == "5":
            try:
                id_buscado = input("\nIntroduce el ID del experimento a recuperar: ")
                datos = servicio.cargar_experimento_en_sesion(id_buscado)
                print(
                    f"✅ Experimento '{datos['nombre']}' (v{datos['version']}) recuperado correctamente."
                )
            except ValueError as e:
                print(f"\n❌ {e}")

        elif opcion == "6":
            print("\nSaliendo de LabTrack... ¡Hasta pronto!")
            servicio.cerrar()
            sys.exit(0)

        else:
            print("\n❌ Opción no válida. Inténtalo de nuevo.")
            logger.warning(f"Opción de menú inválida: {opcion}")


def ejecutar_modo_demo():
    """Ejecuta una demostración completa desatendida para validación rápida en el aula."""
    from src.models.equipamiento import Equipamiento
    from src.models.muestra import Muestra

    print("\n🚀 INICIANDO MODO DEMO AUTOMÁTICO DE LABTRACK...")
    servicio = LaboratorioService.crear_desde_sqlite(":memory:")

    resumen = servicio.iniciar_nueva_sesion(
        "1", "Alonso", "Bioinformática", "Principal", "Síntesis Proteica"
    )
    print(
        f"1. Alta completada -> {resumen['experimento']} (ID: {resumen['id_experimento']})"
    )

    exp = servicio.experimento_activo
    exp.iniciar()
    equipo = Equipamiento("Espectrómetro UV-Vis", limite_usos_mantenimiento=1)
    muestra = Muestra("Reactivo Buffer", cantidad=10.0, unidad="ml", umbral_critico=4.0)

    exp.utilizar_equipamiento(equipo)
    exp.consumir_muestra(muestra, 7.0)
    servicio.experimento_repo.guardar(exp)
    print(
        f"2. Reglas de dominio ejecutadas -> Equipo: '{equipo.estado}' | Stock crítico: {muestra.esta_en_nivel_critico()}"
    )

    bifurcado = servicio.bifurcar_experimento_activo("2.0")
    print(
        f"3. Bifurcación versionada -> Nueva versión: v{bifurcado.version} ({len(bifurcado.historial_eventos)} eventos heredados)"
    )

    ruta_informe = servicio.generar_informe_markdown("informe_demo.md")
    print(f"4. Informe automático generado -> {ruta_informe}")

    servicio.cerrar()
    print("✅ DEMO FINALIZADA CON ÉXITO.\n")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        ejecutar_modo_demo()
    else:
        ejecutar_flujo_principal()
