from flask import Flask, render_template, jsonify, request
from Gabriel.sincronizacion.lectores_escritores import ejecutar as run_lectores
from Gabriel.sincronizacion.cinco_filosofos import ejecutar as run_filosofos

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/lectores_escritores", methods=["GET", "POST"])
def lectores_escritores():
    num_lectores = request.args.get("lectores", 4, type=int)
    num_escritores = request.args.get("escritores", 2, type=int)
    resultado = run_lectores(num_lectores, num_escritores)
    return jsonify(resultado)

@app.route("/cinco_filosofos", methods=["GET", "POST"])
def cinco_filosofos():
    num_filosofos = request.args.get("filosofos", 5, type=int)
    resultado = run_filosofos(num_filosofos)
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)

    