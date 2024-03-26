import sqlite3
import csv
import os
import config

def create_tables(conn):
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS regions (
                region_id INTEGER PRIMARY KEY,
                region_name TEXT NOT NULL
            )''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS locations (
                location_id INTEGER PRIMARY KEY,
                city TEXT NOT NULL,
                residential_rate TEXT NOT NULL,
                summer_start_month INTEGER NOT NULL,
                region_id TEXT NOT NULL,
                FOREIGN KEY (region_id) REFERENCES regions (region_id)
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
            CREATE TABLE IF NOT EXISTS residential_summer_rates(
                charge_id INTEGER PRIMARY KEY,
                rate TEXT NOT NULL,
                billing_period TEXT NOT NULL,
                basic REAL,
                low_intermediate REAL,
                high_intermediate REAL,
                excess REAL,
                UNIQUE(rate, billing_period),
                CHECK (billing_period LIKE '____-__')
            )''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS residential_winter_rates(
                charge_id INTEGER PRIMARY KEY,
                rate TEXT NOT NULL,
                billing_period TEXT NOT NULL,
                basic REAL,
                intermediate REAL,
                excess REAL,
                UNIQUE(rate, billing_period),
                CHECK (billing_period LIKE '____-__')
            )''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS commercial_rates(
                charge_id INTEGER PRIMARY KEY,
                region_id INTEGER NOT NULL,
                rate TEXT NOT NULL,
                billing_period TEXT NOT NULL,
                transmission REAL,
                distribution REAL,
                cenace REAL,
                supplier REAL,
                services REAL,
                energy REAL,
                capacity REAL,
                UNIQUE(region_id, rate, billing_period),
                CHECK (billing_period LIKE '____-__'),
                FOREIGN KEY (region_id) REFERENCES regions (region_id)
            )''')
    except sqlite3.OperationalError as e:
        print(f"Operational error during table creation: {e}")
    except sqlite3.DatabaseError as e:
        print(f"Database error during table creation: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during table creation: {e}")

def execute_bulk_insert(conn, sql, data):
    try:
        with conn:
            conn.executemany(sql, data)
    except sqlite3.IntegrityError as e:
        print(f"Integrity error during bulk insert: {e}")
    except sqlite3.OperationalError as e:
        print(f"Operational error during bulk insert: {e}")
    except sqlite3.ProgrammingError as e:
        print(f"Programming error during bulk insert:: {e}")
    except sqlite3.DataError as e:
        print(f"Data error during bulk insert:: {e}")
    except sqlite3.DatabaseError as e:
        print(f"Database error during bulk insert:: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during bulk insert: {e}")

def populate_table_from_csv(conn, insert_sql, csv_file):
    try:
        with open(csv_file, 'r') as file:
            csv_reader = csv.DictReader(file)
            data_to_insert = [tuple(row.values()) for row in csv_reader]
            execute_bulk_insert(conn, insert_sql, data_to_insert)
    except FileNotFoundError:
        print(f"File not found: {csv_file}")
    except csv.Error as e:
        print(f"CSV error ocurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during CSV processing: {e}")

def populate_tables(conn):
    populate_table_from_csv(conn, "INSERT INTO regions (region_name) VALUES(?)", config.REGIONS_CSV_PATH)
    populate_table_from_csv(conn, "INSERT INTO locations (city, residential_rate, summer_start_month, region_id) VALUES (?, ?, ?, ?)", config.LOCATIONS_CSV_PATH)
    populate_table_from_csv(conn, "INSERT INTO solar_hours (location_id, tilt_angle, month, solar_hours) VALUES (?, ?, ?, ?)", config.SOLAR_HOURS_CSV_PATH)
    populate_table_from_csv(conn, "INSERT INTO residential_summer_rates (rate, billing_period, basic, low_intermediate, high_intermediate, excess) VALUES(?, ?, ?, ?, ?, ?)", config.RESIDENTIAL_SUMMER_RATES_CSV_PATH)
    populate_table_from_csv(conn, "INSERT INTO residential_winter_rates (rate, billing_period, basic, intermediate, excess) VALUES(?, ?, ?, ?, ?)", config.RESIDENTIAL_WINTER_RATES_CSV_PATH)
    populate_table_from_csv(conn, "INSERT INTO commercial_rates (region_id, rate, billing_period, transmission, distribution, cenace, supplier, services, energy, capacity) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", config.COMMERCIAL_RATES_CSV_PATH)
    
def setup_database():
    os.makedirs(os.path.dirname(config.DATABASE_PATH), exist_ok=True)
    
    try:
        with sqlite3.connect(config.DATABASE_PATH) as conn:
            create_tables(conn)
            populate_tables(conn)
            conn.commit()
    except sqlite3.OperationalError as e:
        print(f"Operational error during database setup: {e}")
    except sqlite3.DatabaseError as e:
        print(f"Database error during setup: {e}")
    except Exception as e:
        print(f"An error occurred during setup: {e}")

if __name__ == '__main__':
    setup_database()
