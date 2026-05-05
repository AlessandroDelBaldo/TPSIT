from flask import Flask, render_template, request, jsonify
import json, os

app = Flask(__name__, static_folder='static', template_folder='templates')
DATA_FILE = os.path.join(os.path.dirname(__file__), 'products.json')

@app.route('/')
def index():
    # usa la tua pagina con la form (list.html o products.html)
    return render_template('list.html')

@app.route('/search', methods=['POST'])
def search():
    # legge criteri dalla form (solo campi non vuoti)
    criteria = {k: v for k, v in request.form.items() if v}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        cars = json.load(f)
    def match(car):
        for k, v in criteria.items():
            # accetta chiavi in italiano o inglese (marca/modello/motore/colore)
            val = car.get(k) or car.get(k.lower()) or car.get(k.capitalize()) or ''
            if v.lower() not in str(val).lower():
                return False
        return True
    results = [c for c in cars if match(c)]
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)