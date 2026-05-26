import threading
import time
import random

# ══════════════════════════════════════════
#   PROBLEMA: CENA DE LOS CINCO FILÓSOFOS
#   Autor: Gabriel
#   Descripción: 5 filósofos comen y piensan.
#   Para comer necesitan 2 tenedores.
#   Se evita el deadlock con un semáforo.
# ══════════════════════════════════════════

eventos = []

def filosofo(id, num_filosofos, tenedores, mesa):
    izquierda = id
    derecha = (id + 1) % num_filosofos

    eventos.append(f"[Filósofo {id}] Está pensando...")
    time.sleep(random.uniform(0.01, 0.05))

    eventos.append(f"[Filósofo {id}] Tiene hambre, espera tenedores...")
    mesa.acquire()

    tenedores[izquierda].acquire()
    eventos.append(f"[Filósofo {id}] Tomó tenedor izquierdo ({izquierda})")

    tenedores[derecha].acquire()
    eventos.append(f"[Filósofo {id}] Tomó tenedor derecho ({derecha}) — ¡Comiendo!")

    time.sleep(random.uniform(0.01, 0.05))

    tenedores[derecha].release()
    tenedores[izquierda].release()
    mesa.release()

    eventos.append(f"[Filósofo {id}] Terminó de comer, vuelve a pensar.")

def ejecutar(num_filosofos=5):
    global eventos
    eventos = []
    
    tenedores = [threading.Semaphore(1) for _ in range(num_filosofos)]
    mesa = threading.Semaphore(max(1, num_filosofos - 1))  # máximo n-1 filósofos a la vez para evitar deadlock

    hilos = []
    for i in range(num_filosofos):
        hilos.append(threading.Thread(target=filosofo, args=(i, num_filosofos, tenedores, mesa)))

    for h in hilos:
        h.start()
    for h in hilos:
        h.join()

    eventos.append("✔ Simulación terminada.")
    return eventos