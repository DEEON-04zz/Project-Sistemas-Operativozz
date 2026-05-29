def ejecutar():
    print("\n" + "="*55)
    print("   ALGORITMO DE REEMPLAZO DE PÁGINAS NRU")
    print("   (Not Recently Used — No Usada Recientemente)")
    print("="*55)

    print("""
  ¿Qué es NRU?
  El algoritmo NRU clasifica cada página en memoria
  según dos bits:
    Bit R = Referenciada (se leyó recientemente)
    Bit M = Modificada   (se escribió en ella)

  Esto da 4 clases:
    Clase 0: R=0, M=0  → candidata ideal a salir
    Clase 1: R=0, M=1  → fue modificada pero no leída
    Clase 2: R=1, M=0  → fue leída pero no modificada
    Clase 3: R=1, M=1  → fue leída y modificada (última en salir)

  Cada cierto tiempo el bit R se resetea a 0.
    """)

    marcos   = int(input("¿Cuántos marcos de memoria? (ej: 4): "))
    entrada  = input("Cadena de referencias separadas por espacio (ej: 2 3 2 1 5 2 4 5 3 2 5 2): ")
    refs     = list(map(int, entrada.split()))
    reset_cada = int(input("¿Cada cuántos pasos se resetea el bit R? (ej: 4): "))

    # Cada página en memoria: {'pag': int, 'R': int, 'M': int}
    memoria = []
    fallos  = 0
    aciertos = 0

    print("\n" + "-"*65)
    print(f"{'Paso':<5} {'Ref':<5} {'Memoria (pag,R,M)':<35} {'Clase víctima':<15} {'Fallo'}")
    print("-"*65)

    for i, p in enumerate(refs):

        # Resetear bit R cada ciertos pasos
        if i > 0 and i % reset_cada == 0:
            for pg in memoria:
                pg['R'] = 0

        idx = next((k for k, pg in enumerate(memoria) if pg['pag'] == p), -1)

        if idx != -1:
            # ACIERTO — página ya en memoria
            memoria[idx]['R'] = 1
            aciertos += 1
            mem_str = str([(pg['pag'], pg['R'], pg['M']) for pg in memoria])
            print(f"  {i+1:<4} {p:<5} {mem_str:<35} {'—':<15} No ✓")

        else:
            # FALLO — página no está en memoria
            fallos += 1
            # Asignar bit M aleatorio para simular escrituras (50% de probabilidad)
            import random
            nuevo_M = 1 if random.random() > 0.5 else 0

            if len(memoria) < marcos:
                # Hay espacio — agregar directo
                memoria.append({'pag': p, 'R': 1, 'M': nuevo_M})
                clase_victima = '—'
            else:
                # Memoria llena — buscar víctima por clase más baja
                victima_idx = -1
                clase_victima = ''

                for clase in range(4):
                    for k, pg in enumerate(memoria):
                        R, M = pg['R'], pg['M']
                        clase_pg = R * 2 + M
                        if clase_pg == clase:
                            victima_idx = k
                            clase_victima = f'Clase {clase}'
                            break
                    if victima_idx != -1:
                        break

                memoria[victima_idx] = {'pag': p, 'R': 1, 'M': nuevo_M}

            mem_str = str([(pg['pag'], pg['R'], pg['M']) for pg in memoria])
            print(f"  {i+1:<4} {p:<5} {mem_str:<35} {clase_victima:<15} Sí ❌")

    print("-"*65)
    print(f"\n  Total de referencias : {len(refs)}")
    print(f"  Fallos de página     : {fallos}")
    print(f"  Aciertos             : {aciertos}")
    print(f"  Tasa de fallos       : {fallos/len(refs)*100:.1f}%")
    print(f"\n  Clases NRU:")
    print(f"  {'Página':<8} {'R':<5} {'M':<5} {'Clase'}")
    print(f"  {'-'*25}")
    for pg in memoria:
        clase = pg['R']*2 + pg['M']
        print(f"  {pg['pag']:<8} {pg['R']:<5} {pg['M']:<5} Clase {clase}")
    print()

ejecutar()