import threading
import time
import random

mutex = threading.Semaphore(1)
escritura = threading.Semaphore(1)
lectores_activos = 0
recurso = "dato_inicial"
eventos = []

def lector(id_lector):
    global lectores_activos, recurso

    eventos.append(f"[Lector {id_lector}] Quiere leer...")
    time.sleep(random.uniform(0.01, 0.05))

    mutex.acquire()
    lectores_activos += 1
    if lectores_activos == 1:
        escritura.acquire()
    mutex.release()

    eventos.append(f"[Lector {id_lector}] Leyendo: '{recurso}' (lectores activos: {lectores_activos})")
    time.sleep(random.uniform(0.01, 0.05))

    mutex.acquire()
    lectores_activos -= 1
    if lectores_activos == 0:
        escritura.release()
    mutex.release()

    eventos.append(f"[Lector {id_lector}] Terminó de leer.")

def escritor(id_escritor):
    global recurso

    eventos.append(f"[Escritor {id_escritor}] Quiere escribir...")
    time.sleep(random.uniform(0.01, 0.05))

    escritura.acquire()
    recurso = f"dato_escrito_por_escritor_{id_escritor}"
    eventos.append(f"[Escritor {id_escritor}] Escribiendo: '{recurso}'")
    time.sleep(random.uniform(0.01, 0.05))
    escritura.release()

    eventos.append(f"[Escritor {id_escritor}] Terminó de escribir.")

def ejecutar():
    global lectores_activos, recurso, eventos
    lectores_activos = 0
    recurso = "dato_inicial"
    eventos = []

    hilos = []
    for i in range(1, 5):
        hilos.append(threading.Thread(target=lector, args=(i,)))
    for i in range(1, 3):
        hilos.append(threading.Thread(target=escritor, args=(i,)))

    random.shuffle(hilos)
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()

    eventos.append("✔ Simulación terminada.")
    return eventos