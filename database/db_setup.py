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

def setup_database(db_path=config.DATABASE_PATH, locations_csv='data/locations.csv', solar_hours_csv='data/solar_hours.csv'):
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

            # Populate tables
            populate_locations(conn, locations_csv)
            populate_solar_hours(conn, solar_hours_csv)

            conn.commit()
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred during setup: {e}")

def initialize_database():
    db_path = 'data/SolarData.db'
    locations_csv = 'data/locations.csv'
    solar_hours_csv = 'data/solar_hours.csv'

    setup_database(db_path, locations_csv, solar_hours_csv)

if __name__ == '__main__':
    initialize_database()
