import sqlite3
import re
import os

SQL_PATH = os.path.join(os.path.dirname(__file__), '..', 'localita.sql')

def init_db():
    conn = sqlite3.connect('comuni.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS comuni
                 (ID INTEGER PRIMARY KEY, name TEXT, slug TEXT, lat REAL, lng REAL,
                  codice_provincia_istat TEXT, codice_comune_istat TEXT,
                  codice_alfanumerico_istat TEXT, capoluogo_provincia INTEGER, capoluogo_regione INTEGER)''')
    
    # Parse SQL dump
    with open(SQL_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    values = []
    parsing_insert = False
    for line in lines:
        line = line.strip()
        if 'INSERT INTO `comuni` (' in line:
            parsing_insert = True
            continue
        if parsing_insert and line.endswith(';'):
            # Extract VALUES part
            match = re.search(r'VALUES\s*\((.+?)\)', line)
            if match:
                vals_str = match.group(1)
                vals = [v.strip().strip("'\"") for v in vals_str.split(',')]
                if len(vals) == 10:
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
            parsing_insert = False
        elif parsing_insert and '(' in line and not line.startswith('('):
            # Multi-line VALUES
            continue
    
    c.executemany('INSERT OR REPLACE INTO comuni VALUES (?,?,?,?,?,?,?,?,?)', values)
    conn.commit()
    conn.close()
    print(f"Imported {len(values)} comuni.")

if __name__ == '__main__':
    init_db()

