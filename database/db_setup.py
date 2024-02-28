import sqlite3
import csv
import os
import config

def execute_bulk_insert(conn, sql, data):
    try:
        conn.executemany(sql, data)
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def populate_table_from_csv(conn, insert_sql, csv_file):
    try:
        with open(csv_file, 'r') as file:
            csv_reader = csv.DictReader(file)
            data_to_insert = [tuple(row.values()) for row in csv_reader]
            execute_bulk_insert(conn, insert_sql, data_to_insert)
    except FileNotFoundError:
        print(f"File not found: {csv_file}")

def setup_database():
    os.makedirs(os.path.dirname(config.DATABASE_PATH), exist_ok=True)
    
    try:
        with sqlite3.connect(config.DATABASE_PATH) as conn:
            # Create tables
            conn.execute('''
                CREATE TABLE IF NOT EXISTS locations (
                    location_id INTEGER PRIMARY KEY,
                    city TEXT NOT NULL,
                    state TEXT NOT NULL
                )''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS solar_hours (
                    solar_hour_id INTEGER PRIMARY KEY,
                    location_id INTEGER,
                    tilt_angle INTEGER,
                    month INTEGER,
                    solar_hours REAL NOT NULL,
                    FOREIGN KEY (location_id) REFERENCES locations (location_id)
                )''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS pdbt_rate(
                    rate_id INTEGER PRIMARY KEY,
                    state TEXT NOT NULL,
                    billing_period TEXT NOT NULL,
                    transmission REAL,
                    distribution REAL,
                    cenace REAL,
                    supplier REAL,
                    services REAL,
                    energy REAL,
                    capacity REAL,
                    UNIQUE(state, billing_period),
                    CHECK (billing_period LIKE '____-__')
                )''')

            # Populate tables using the paths from the config module
            populate_table_from_csv(conn, "INSERT INTO locations (city, state) VALUES (?, ?)", config.LOCATIONS_CSV_PATH)
            populate_table_from_csv(conn, "INSERT INTO solar_hours (location_id, tilt_angle, month, solar_hours) VALUES (?, ?, ?, ?)", config.SOLAR_HOURS_CSV_PATH)
            populate_table_from_csv(conn, "INSERT INTO pdbt_rate (state, billing_period, transmission, distribution, cenace, supplier, services, energy, capacity) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", config.PDBT_RATE_CSV_PATH)
            
            conn.commit()
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred during setup: {e}")

if __name__ == '__main__':
    setup_database()
