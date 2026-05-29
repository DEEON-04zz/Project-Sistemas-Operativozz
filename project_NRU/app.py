from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__, static_folder='static')
def algoritmo_nru(marcos, referencias, reset_cada):
    memoria = []
    fallos = 0
    aciertos = 0
    pasos = []

    for i, p in enumerate(referencias):

        # Resetear bit R cada N pasos
        if i > 0 and i % reset_cada == 0:
            for pg in memoria:
                pg['R'] = 0
            pasos.append({'tipo': 'reset'})

        idx = next((k for k, pg in enumerate(memoria) if pg['pag'] == p), -1)

        if idx != -1:
            # ACIERTO
            memoria[idx]['R'] = 1
            aciertos += 1
            c = memoria[idx]['R'] * 2 + memoria[idx]['M']
            pasos.append({
                'tipo': 'acierto',
                'pagina': p,
                'clase': c,
                'memoria': [dict(pg) for pg in memoria]
            })

        else:
            # FALLO
            fallos += 1
            M = random.randint(0, 1)

            if len(memoria) < marcos:
                memoria.append({'pag': p, 'R': 1, 'M': M})
                pasos.append({
                    'tipo': 'fallo_espacio',
                    'pagina': p,
                    'clase': '—',
                    'memoria': [dict(pg) for pg in memoria]
                })
            else:
                victima_idx = -1
                clase_victima = 0
                for clase in range(4):
                    for k, pg in enumerate(memoria):
                        if pg['R'] * 2 + pg['M'] == clase:
                            victima_idx = k
                            clase_victima = clase
                            break
                    if victima_idx != -1:
                        break

                victima_pag = memoria[victima_idx]['pag']
                memoria[victima_idx] = {'pag': p, 'R': 1, 'M': M}
                pasos.append({
                    'tipo': 'fallo_reemplazo',
                    'pagina': p,
                    'victima': victima_pag,
                    'clase_victima': clase_victima,
                    'memoria': [dict(pg) for pg in memoria]
                })

    return {
        'pasos': pasos,
        'fallos': fallos,
        'aciertos': aciertos,
        'tasa': round(fallos / len(referencias) * 100, 1),
        'memoria_final': memoria
    }


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ejecutar', methods=['POST'])
def ejecutar():
    datos = request.get_json()
    marcos = int(datos['marcos'])
    referencias = list(map(int, datos['referencias'].split()))
    reset_cada = int(datos['reset_cada'])
    resultado = algoritmo_nru(marcos, referencias, reset_cada)
    return jsonify(resultado)


if __name__ == '__main__':
    app.run(debug=True)