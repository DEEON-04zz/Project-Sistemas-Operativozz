from flask import Flask, render_template, jsonify
from sincronizacion.lectores_escritores import ejecutar as run_lectores
from sincronizacion.cinco_filosofos import ejecutar as run_filosofos

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/lectores_escritores")
def lectores_escritores():
    resultado = run_lectores()
    return jsonify(resultado)

@app.route("/cinco_filosofos")
def cinco_filosofos():
    resultado = run_filosofos()
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)

    