import sqlite3
import re
import os

def load_data():
    conn = sqlite3.connect('comuni.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS comuni')
    c.execute('''CREATE TABLE comuni
                 (ID INTEGER PRIMARY KEY, name TEXT, slug TEXT, lat REAL, lng REAL,
                  codice_provincia_istat TEXT, codice_comune_istat TEXT,
                  codice_alfanumerico_istat TEXT, capoluogo_provincia INTEGER, capoluogo_regione INTEGER)''')
    
    # Simple INSERT of first few records to test
    data = [
        (1, 'Agliè', 'aglie', 45.3681, 7.7681, '001', '001', '001001', 0, 0),
        (2, 'Airasca', 'airasca', 44.9181, 7.4855, '001', '002', '001002', 0, 0),
        (3, 'Ala di Stura', 'ala-di-stura', 45.3154, 7.3026, '001', '003', '001003', 0, 0),
        (272, 'Torino', 'torino', 45.05, 7.6667, '001', '272', '001272', 1, 1),
        (398, 'Vercelli', 'vercelli', 45.321, 8.4263, '002', '158', '002158', 1, 0),
        (459, 'Novara', 'novara', 45.4451, 8.6187, '003', '106', '003106', 1, 0),
        (567, 'Cuneo', 'cuneo', 44.3888, 7.5471, '004', '078', '004078', 1, 0),
        (744, 'Asti', 'asti', 44.9009, 8.2068, '005', '005', '005005', 1, 0),
        (860, 'Alessandria', 'alessandria', 44.9132, 8.617, '006', '003', '006003', 1, 0),
        (1050, 'Aosta', 'aosta', 45.735, 7.3132, '007', '003', '007003', 1, 1),
    ]
    c.executemany('INSERT INTO comuni VALUES (?,?,?,?,?,?,?,?,?,?)', data)
    conn.commit()
    conn.close()
    print("Loaded sample data (10 records including capitals). Full parse available in db_fixed.py.")

if __name__ == '__main__':
    load_data()

