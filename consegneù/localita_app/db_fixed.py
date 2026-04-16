import sqlite3
import re
import os

SQL_PATH = 'c:/Users/Utente/TPSIT/consegneù/localita.sql'

def init_db():
    conn = sqlite3.connect('comuni.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS comuni')
    c.execute('''CREATE TABLE comuni
                 (ID INTEGER PRIMARY KEY, name TEXT, slug TEXT, lat REAL, lng REAL,
                  codice_provincia_istat TEXT, codice_comune_istat TEXT,
                  codice_alfanumerico_istat TEXT, capoluogo_provincia INTEGER, capoluogo_regione INTEGER)''')
    
    # Parse SQL dump
    with open(SQL_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract all INSERT VALUES
    pattern = r"INSERT INTO `comuni`\s*\([^)]*\)\s*VALUES\s*\(([^\)]*?)\)"
    matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
    
    values = []
    for match in matches:
        vals_str = match.strip()
        vals = [v.strip().strip("'\"") for v in vals_str.split(',')]
        if len(vals) == 10:
            try:
                id_val = int(vals[0])
                name = vals[1].replace("'", "''")
                slug = vals[2].replace("'", "''")
                lat = float(vals[3])
                lng = float(vals[4])
                prov = vals[5]
                com = vals[6]
                alf = vals[7]
                cap_prov = int(vals[8])
                cap_reg = int(vals[9])
                values.append((id_val, name, slug, lat, lng, prov, com, alf, cap_prov, cap_reg))
            except (ValueError, IndexError):
                continue
    
    c.executemany('INSERT OR IGNORE INTO comuni VALUES (?,?,?,?,?,?,?,?,?,?)', values)
    conn.commit()
    conn.close()
    print(f"Imported {len(values)} comuni.")

if __name__ == '__main__':
    init_db()

