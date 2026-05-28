def ejecutar():
    print("\n=== Reemplazo de Páginas Óptimo ===\n")

    marcos = int(input("¿Cuántos marcos de memoria? (ej: 3): "))
    entrada = input("Ingrese la cadena de referencias separadas por espacio (ej: 7 0 1 2 0 3 0 4): ")
    referencias = list(map(int, entrada.split()))

    memoria = []
    fallos = 0

    print("\nReferencia | Memoria              | Fallo")
    print("-" * 50)

    for i, pagina in enumerate(referencias):
        if pagina in memoria:
            estado = "No"
        else:
            fallos += 1
            estado = "Sí"

            if len(memoria) < marcos:
                memoria.append(pagina)
            else:
                futuro = []
                for p in memoria:
                    if p in referencias[i+1:]:
                        futuro.append(referencias[i+1:].index(p))
                    else:
                        futuro.append(float('inf'))

                reemplazar = futuro.index(max(futuro))
                memoria[reemplazar] = pagina

        print(f"     {pagina}         | {str(memoria).ljust(20)} | {estado}")

    print("-" * 50)
    print(f"\nTotal de fallos de página: {fallos}")
    print(f"Total de aciertos:         {len(referencias) - fallos}")

ejecutar()