import sqlite3
from database.dao_interface import SolarHoursDAO
import config

class SolarHoursData(SolarHoursDAO):
    def __init__(self, db_path=config.DATABASE_PATH):
        self.db_path = db_path

    def get_solar_hours(self, city, tilt):
        try:
            with sqlite3.connect((self.db_path)) as conn:
                cursor = conn.cursor()
                query = """
                SELECT solar_hours
                FROM solar_hours
                JOIN locations ON solar_hours.location_id = locations.location_id
                WHERE city = ?
                AND tilt_angle = ?
                ORDER BY month
                """
                cursor.execute(query, (city, tilt))
                result = cursor.fetchall()
                return [row[0] for row in result] if result else None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            import traceback
            traceback.print_exc()
            return None