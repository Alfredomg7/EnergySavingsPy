import sqlite3
import csv
import os
import config

def populate_locations(conn, locations_csv):
    try:
        with open(locations_csv, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                conn.execute('''INSERT INTO locations (location_id, location_name)
                                VALUES (?, ?)''',
                             (row['location_id'], row['location_name']))
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
    except FileNotFoundError:
        print(f"File not found: {locations_csv}")
    except Exception as e:
        print(f"An error occurred: {e}")

def populate_solar_hours(conn, solar_hours_csv):
    try:
        with open(solar_hours_csv, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                conn.execute('''INSERT INTO solar_hours (location_id, tilt_angle, month, solar_hours)
                                VALUES (?, ?, ?, ?)''',
                             (row['location_id'], row['tilt_angle'], row['month'], row['solar_hours']))
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
    except FileNotFoundError:
        print(f"File not found: {solar_hours_csv}")
    except Exception as e:
        print(f"An error occurred: {e}")

def populate_pdbt_rate(conn, pdbt_rate_csv):
    try:
        with open(pdbt_rate_csv, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                conn.execute('''INSERT INTO pdbt_rate (billing_period, transmission, distribution, cenace, supplier, services, energy, capacity)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                             (row['billing_period'], row['transmission'], row['distribution'], row['cenace'], row['supplier'], row['services'], row['energy'], row['capacity']))
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
    except FileNotFoundError:
        print(f"File not found: {pdbt_rate_csv}")
    except Exception as e:
        print(f"An error occurred: {e}")

def setup_database(db_path=config.DATABASE_PATH, locations_csv='data/locations.csv', solar_hours_csv='data/solar_hours.csv', pdbt_rate_csv='data/pdbt_rate.csv'):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    try:
        with sqlite3.connect(db_path) as conn:
            # Create the locations table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS locations (
                    location_id INTEGER PRIMARY KEY,
                    location_name TEXT NOT NULL
                )
            ''')

            # Create the solar_hours table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS solar_hours (
                    solar_hour_id INTEGER PRIMARY KEY,
                    location_id INTEGER,
                    tilt_angle INTEGER,
                    month INTEGER,
                    solar_hours REAL NOT NULL,
                    FOREIGN KEY (location_id) REFERENCES locations (location_id)
                )
            ''')
            
            # Create the pdbt_rate table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS pdbt_rate(
                    billing_period_id INTEGER PRIMARY KEY,
                    billing_period TEXT NOT NULL,
                    transmission REAL,
                    distribution REAL,
                    cenace REAL,
                    supplier REAL,
                    services REAL,
                    energy REAL,
                    capacity REAL,
                    UNIQUE(billing_period),
                    CHECK (billing_period LIKE '____-__')
                )
            ''')

            # Populate tables
            populate_locations(conn, locations_csv)
            populate_solar_hours(conn, solar_hours_csv)
            populate_pdbt_rate(conn, pdbt_rate_csv)
            conn.commit()
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred during setup: {e}")

if __name__ == '__main__':
    setup_database()
