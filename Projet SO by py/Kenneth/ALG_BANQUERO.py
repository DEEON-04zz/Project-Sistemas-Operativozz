def ejecutar():
    print("\n=== Algoritmo del Banquero ===\n")

    n = int(input("¿Cuántos procesos? (ej: 3): "))
    r = int(input("¿Cuántos tipos de recursos? (ej: 1): "))

    print("\nIngrese la asignación actual de cada proceso:")
    asignacion = []
    for i in range(n):
        fila = list(map(int, input(f"  Proceso {i}: ").split()))
        asignacion.append(fila)

    print("\nIngrese la necesidad máxima de cada proceso:")
    maximo = []
    for i in range(n):
        fila = list(map(int, input(f"  Proceso {i}: ").split()))
        maximo.append(fila)

    print("\nIngrese los recursos disponibles actualmente:")
    disponible = list(map(int, input("  Disponible: ").split()))

    necesidad = []
    for i in range(n):
        fila = []
        for j in range(r):
            fila.append(maximo[i][j] - asignacion[i][j])
        necesidad.append(fila)

    print("\n--- Estado Inicial ---")
    print(f"{'Proceso':<10} {'Asignado':<15} {'Máximo':<15} {'Necesidad':<15}")
    print("-" * 55)
    for i in range(n):
        print(f"  P{i:<8} {str(asignacion[i]):<15} {str(maximo[i]):<15} {str(necesidad[i]):<15}")
    print(f"\nDisponible: {disponible}")

    trabajo = disponible[:]
    terminado = [False] * n
    secuencia = []

    print("\n--- Buscando secuencia segura ---")

    encontrado = True
    while encontrado:
        encontrado = False
        for i in range(n):
            if not terminado[i]:
                puede = True
                for j in range(r):
                    if necesidad[i][j] > trabajo[j]:
                        puede = False
                        break
                if puede:
                    print(f"  ✓ Proceso P{i} puede terminar → libera {asignacion[i]}")
                    for j in range(r):
                        trabajo[j] += asignacion[i][j]
                    terminado[i] = True
                    secuencia.append(i)
                    encontrado = True

    print("\n--- Resultado ---")
    if all(terminado):
        print(f"  ✅ Estado SEGURO")
        print(f"  Secuencia segura: {' → '.join(['P'+str(i) for i in secuencia])}")
    else:
        print(f"  ❌ Estado INSEGURO — riesgo de deadlock")
        pendientes = [f"P{i}" for i in range(n) if not terminado[i]]
        print(f"  Procesos bloqueados: {', '.join(pendientes)}")

    print(f"\nRecursos finales disponibles: {trabajo}")

ejecutar()