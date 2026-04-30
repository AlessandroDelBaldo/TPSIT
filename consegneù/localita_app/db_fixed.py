import sqlite3
import re
import os

SQL_PATH = 'c:/Users/Utente/TPSIT/consegneù/localita.sql'

def init_db():
    if not os.path.exists(SQL_PATH):
        print(f"SQL file not found: {SQL_PATH}")
        return

    conn = sqlite3.connect('comuni.db')
    c = conn.cursor()

    with open(SQL_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # First, try to execute the dump directly (preferred)
    try:
        conn.executescript(content)
        try:
            c.execute('SELECT COUNT(*) FROM comuni')
            count = c.fetchone()[0] or 0
        except sqlite3.OperationalError:
            count = 0
        print(f"Imported {count} comuni via executescript.")
        conn.commit()
        conn.close()
        return
    except sqlite3.Error:
        # Fall back to manual parsing below
        pass

    # Recreate table with the expected 10 columns
    c.execute('DROP TABLE IF EXISTS comuni')
    c.execute('''CREATE TABLE comuni
                 (ID INTEGER PRIMARY KEY, name TEXT, slug TEXT, lat REAL, lng REAL,
                  codice_provincia_istat TEXT, codice_comune_istat TEXT,
                  codice_alfanumerico_istat TEXT, capoluogo_provincia INTEGER, capoluogo_regione INTEGER)''')

    # Find INSERT blocks (may contain multiple tuples)
    blocks = re.findall(r"INSERT INTO `comuni`\s*\([^)]*\)\s*VALUES\s*(.+?);", content, re.DOTALL | re.IGNORECASE)

    values = []
    for block in blocks:
        # extract each parenthesized tuple
        tuples = re.findall(r"\((?:[^()]*)\)", block, re.DOTALL)
        for t in tuples:
            vals_str = t[1:-1].strip()
            # split into fields: match quoted strings (with doubled '') or NULL or unquoted tokens
            parts = re.findall(r"'(?:[^']|'')*'|NULL|[^,]+", vals_str, re.DOTALL)
            parsed = []
            for p in parts:
                p = p.strip()
                if p.upper() == 'NULL':
                    parsed.append(None)
                elif p.startswith("'") and p.endswith("'"):
                    parsed.append(p[1:-1].replace("''", "'"))
                else:
                    parsed.append(p)

            # Normalize to 10 fields: if 9 fields, assume missing last (capoluogo_regione)
            if len(parsed) == 9:
                parsed.append(None)
            if len(parsed) != 10:
                continue

            try:
                id_val = int(parsed[0]) if parsed[0] is not None and parsed[0] != '' else None
                name = parsed[1]
                slug = parsed[2]
                lat = float(parsed[3]) if parsed[3] not in (None, '', 'NULL') else None
                lng = float(parsed[4]) if parsed[4] not in (None, '', 'NULL') else None
                prov = parsed[5]
                com = parsed[6]
                alf = parsed[7]
                cap_prov = int(parsed[8]) if parsed[8] not in (None, '', 'NULL') else 0
                cap_reg = int(parsed[9]) if parsed[9] not in (None, '', 'NULL') else 0
                values.append((id_val, name, slug, lat, lng, prov, com, alf, cap_prov, cap_reg))
            except (ValueError, TypeError):
                continue

    if values:
        c.executemany('INSERT OR IGNORE INTO comuni VALUES (?,?,?,?,?,?,?,?,?,?)', values)
        conn.commit()

    print(f"Imported {len(values)} comuni (fallback parser).")
    conn.close()

if __name__ == '__main__':
    init_db()

