import sqlite3
from database.dao_interface import LocationDAO
import config

class LocationData(LocationDAO):
    def __init__(self, db_path=config.DATABASE_PATH):
        self.db_path = db_path

    def get_region_id(self, city):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = """
                    SELECT region_id
                    FROM locations WHERE city = ?
                """
                cursor.execute(query, (city,))
                result = cursor.fetchone()
                return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        
    def get_region(self, city):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = """
                    SELECT region_name
                    FROM regions
                    JOIN locations
                    ON regions.region_id = locations.region_id
                    WHERE city = ?
                """
                cursor.execute(query, (city,))
                result = cursor.fetchone()
                return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None