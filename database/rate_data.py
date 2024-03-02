import sqlite3
from database.dao_interface import PdbtRateDAO
import config

class PdbtRateData(PdbtRateDAO):
    def __init__(self, db_path=config.DATABASE_PATH):
        self.db_path = db_path

    def get_charges(self, state):
        try:
            with sqlite3.connect((self.db_path)) as conn:
                cursor = conn.cursor()
                query = """
                    SELECT billing_period, transmission, distribution, cenace, supplier, services, energy, capacity
                    FROM pdbt_rate
                    WHERE state = ?
                """
                cursor.execute(query, (state,))
                result = cursor.fetchall()
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in result] if result else None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            import traceback
            traceback.print_exc()
            return None