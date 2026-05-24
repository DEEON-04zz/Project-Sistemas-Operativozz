# ══════════════════════════════════════════
#   PROYECTO: Algoritmos de SO
#   Grupo #4
#   Gabriel → Sincronización y Concurrencia
# ══════════════════════════════════════════

from sincronizacion.lectores_escritores import ejecutar as lectores_escritores

def menu():
    while True:
        print("\n╔══════════════════════════════════════════╗")
        print("║       SISTEMAS OPERATIVOS - GRUPO 4      ║")
        print("╠══════════════════════════════════════════╣")
        print("║  GABRIEL - Sincronización                ║")
        print("║    1. Lectores y Escritores              ║")
        print("║    2. Cena de los Cinco Filósofos        ║")
        print("╠══════════════════════════════════════════╣")
        print("║    0. Salir                              ║")
        print("╚══════════════════════════════════════════╝")

        opcion = input("\nElige una opción: ")

        if opcion == "1":
            lectores_escritores()
        elif opcion == "2":
            print("\n⏳ Cinco Filósofos - Próximamente...")
        elif opcion == "0":
            print("\n👋 Saliendo...\n")
            break
        else:
            print("\n❌ Opción inválida.")

if __name__ == "__main__":
    menu()