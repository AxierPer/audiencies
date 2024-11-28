import sqlite3

def connection():
    conn = sqlite3.connect("data_audiencias.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audiencias(
        id INTEGER PRIMARY KEY  AUTOINCREMENT,
        zipcode TEXT,
        latitude REAL,
        longitude REAL,
        city TEXT,
        state_id TEXT,
        state_name TEXT,
        density REAL,
        county_fips REAL,
        county_name TEXT,
        timezone TEXT,
        hispanos_in_us INTEGER,
        population INTEGER
    )
    """)

    return conn
