from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return render_template('products.html')

@app.route('/api/cars', methods=['POST'])
def get_cars():
    data = request.json
    brand = data.get('brand', '').lower()
    model = data.get('model', '').lower()
    fuel_type = data.get('fuel_type', '').lower()
    color = data.get('color', '').lower()

    with open(os.path.join(BASE_DIR, 'products.json')) as f:
        cars = json.load(f)

    filtered_cars = [
        car for car in cars
        if (brand in car['brand'].lower() and
            model in car['model'].lower() and
            fuel_type in car['fuel_type'].lower() and
            color in car['color'].lower())
    ]

    return jsonify(filtered_cars)

if __name__ == '__main__':
    app.run(debug=True, port=7000)