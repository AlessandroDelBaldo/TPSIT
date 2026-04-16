from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

DB_PATH = 'comuni.db'

@app.route('/')
def home():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM comuni")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM comuni WHERE capoluogo_provincia=1")
    cap_prov = c.fetchone()[0]
    conn.close()
    return render_template('index.html', total=total, cap_prov=cap_prov)

@app.route('/search')
def search():
    q = request.args.get('q', '').lower()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM comuni WHERE LOWER(name) LIKE ? OR LOWER(slug) LIKE ?", (f'%{q}%', f'%{q}%'))
    results = c.fetchall()
    conn.close()
    return render_template('results.html', results=results, q=q)

@app.route('/provincia/<prov>')
def provincia(prov):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM comuni WHERE codice_provincia_istat=?", (prov,))
    count = c.fetchone()[0]
    c.execute("SELECT * FROM comuni WHERE codice_provincia_istat=? LIMIT 50", (prov,))
    results = c.fetchall()
    conn.close()
    return render_template('provincia.html', prov=prov, count=count, results=results)

@app.route('/capoluoghi')
def capoluoghi():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM comuni WHERE capoluogo_provincia=1 OR capoluogo_regione=1 ORDER BY name")
    results = c.fetchall()
    conn.close()
    return render_template('capoluoghi.html', results=results)

@app.route('/map/<int:com_id>')
def map_view(com_id):
    return render_template('map.html', comune_id=com_id)

@app.route('/api/comune/<int:com_id>')
def api_comune(com_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM comuni WHERE ID=?", (com_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return jsonify(dict(zip(['ID', 'name', 'slug', 'lat', 'lng', 'codice_provincia_istat', 'codice_comune_istat', 'codice_alfanumerico_istat', 'capoluogo_provincia', 'capoluogo_regione'], row)))
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

