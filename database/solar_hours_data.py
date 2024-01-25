import sqlite3
from database.dao_interface import SolarHoursDAO

class SolarHoursData(SolarHoursDAO):
    def __init__(self, db_path='SolarData.db'):
        self.db_path = db_path

    def get_solar_hours(self, location_name, tilt):
        try:
            with sqlite3.connect((self.db_path)) as conn:
                cursor = conn.cursor()
                query = """
                SELECT month, solar_hours
                FROM solar_hours
                JOIN locations ON solar_hours.location_id = locations.location_id
                WHERE location_name = ?
                AND tilt_angle = ?
                ORDER BY month
                """
                cursor.execute(query, (location_name, tilt))
                result = cursor.fetchall()
                return {row[0]: row[1] for row in result} if result else None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            import traceback
            traceback.print_exc()
            return None

