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

NUM_FILOSOFOS = 5
tenedores = [threading.Semaphore(1) for _ in range(NUM_FILOSOFOS)]
mesa = threading.Semaphore(4)  # máximo 4 filósofos a la vez para evitar deadlock
eventos = []

def filosofo(id):
    izquierda = id
    derecha = (id + 1) % NUM_FILOSOFOS

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

def ejecutar():
    global eventos
    eventos = []

    hilos = []
    for i in range(NUM_FILOSOFOS):
        hilos.append(threading.Thread(target=filosofo, args=(i,)))

    for h in hilos:
        h.start()
    for h in hilos:
        h.join()

    eventos.append("✔ Simulación terminada.")
    return eventos