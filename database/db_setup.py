import sqlite3

def setup_database(db_path='SolarData.db'):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS locations (
                location_id INTEGER PRIMARY KEY,
                location_name TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS solar_hours (
                solar_hour_id INTEGER PRIMARY KEY,
                location_id INTEGER,
                tilt_angle INTEGER,
                month INTEGER,
                solar_hours REAL NOT NULL,
                FOREIGN KEY (location_id) REFERENCES locations (location_id)
            )
        ''')

        conn.commit()

if __name__ == '__main__':
    setup_database()
