# app.py
from flask import Flask, render_template, request, jsonify
from nutriscore_calculator import calculer_nutriscore

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calcul', methods=['POST'])
def calcul():
    data = request.json
    result = calculer_nutriscore(
        energie_kj=float(data.get('energie_kj', 0)),
        acides_gras=float(data.get('acides_gras', 0)),
        sucres=float(data.get('sucres', 0)),
        sodium_mg=float(data.get('sodium', 0)),
        proteines=float(data.get('proteines', 0)),
        fibres=float(data.get('fibres', 0)),
        fruits_legumes=float(data.get('fruits_legumes', 0))
    )
    return jsonify(result)

if __name__ == "__main__":
    print("🚀 Lancement du serveur Flask sur http://127.0.0.1:5000 ...")
    app.run(debug=True)
    print("✅ app.py chargé avec succès !", flush=True)

