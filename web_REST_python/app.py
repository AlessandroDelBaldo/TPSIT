import json
import re
import os
from flask import Flask, request, jsonify, render_template, url_for, redirect

app = Flask(__name__)

USERS_FILE = os.path.join(os.path.dirname(__file__), 'users.json')

ID_PATTERN = re.compile(r'^\d+$')
NAME_PATTERN = re.compile(r'^[A-Za-zÀ-ÿ\s]{2,50}$')
DATE_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}$')
ROLE_PATTERN = re.compile(r'^[A-Za-zÀ-ÿ\s]{2,100}$')


def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def next_id(users):
    if not users:
        return 1
    return max(u['id'] for u in users) + 1


def validate_user(data):
    errors = []
    if not data.get('nome') or not NAME_PATTERN.match(data['nome'].strip()):
        errors.append('Nome non valido (solo lettere, 2-50 caratteri)')
    if not data.get('cognome') or not NAME_PATTERN.match(data['cognome'].strip()):
        errors.append('Cognome non valido (solo lettere, 2-50 caratteri)')
    if not data.get('data_nascita') or not DATE_PATTERN.match(data['data_nascita']):
        errors.append('Data di nascita non valida (formato YYYY-MM-DD)')
    if not data.get('mansione') or not ROLE_PATTERN.match(data['mansione'].strip()):
        errors.append('Mansione non valida (solo lettere, 2-100 caratteri)')
    return errors

@app.route('/')
def home():
    return redirect(url_for('index'))

@app.route('/gestionale_utenti/')
def index():
    return render_template('index.html')


@app.route('/gestionale_utenti/users/', methods=['GET', 'POST'])
def users_collection():
    if request.method == 'GET':
        return jsonify(load_users()), 200

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Corpo della richiesta non valido'}), 400
        errors = validate_user(data)
        if errors:
            return jsonify({'errors': errors}), 400
        users_list = load_users()
        new_user = {
            'id': next_id(users_list),
            'nome': data['nome'].strip(),
            'cognome': data['cognome'].strip(),
            'data_nascita': data['data_nascita'],
            'mansione': data['mansione'].strip()
        }
        users_list.append(new_user)
        save_users(users_list)
        return jsonify(new_user), 201

    return jsonify({'error': 'Metodo non consentito'}), 405


@app.route('/gestionale_utenti/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_resource(user_id):
    if not ID_PATTERN.match(user_id):
        return jsonify({'error': 'ID non valido'}), 400

    uid = int(user_id)
    users_list = load_users()
    user = next((u for u in users_list if u['id'] == uid), None)

    if request.method == 'GET':
        if not user:
            return jsonify({'error': 'Utente non trovato'}), 404
        return jsonify(user), 200

    if request.method == 'PUT':
        if not user:
            return jsonify({'error': 'Utente non trovato'}), 404
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Corpo della richiesta non valido'}), 400
        errors = validate_user(data)
        if errors:
            return jsonify({'errors': errors}), 400
        user['nome'] = data['nome'].strip()
        user['cognome'] = data['cognome'].strip()
        user['data_nascita'] = data['data_nascita']
        user['mansione'] = data['mansione'].strip()
        save_users(users_list)
        return jsonify(user), 200

    if request.method == 'DELETE':
        if not user:
            return jsonify({'error': 'Utente non trovato'}), 404
        users_list = [u for u in users_list if u['id'] != uid]
        save_users(users_list)
        return jsonify({'message': 'Utente eliminato con successo'}), 200

    return jsonify({'error': 'Metodo non consentito'}), 405


if __name__ == '__main__':
    app.run(debug=True, port='5000')
