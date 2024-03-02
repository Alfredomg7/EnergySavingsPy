import sqlite3
from database.dao_interface import PdbtRateDAO
import config

class PdbtRateData(PdbtRateDAO):
    def __init__(self, db_path=config.DATABASE_PATH):
        self.db_path = db_path

    def get_charges(self, state, start_month, end_month):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = """
                    SELECT billing_period, transmission, distribution, cenace, supplier, services, energy, capacity
                    FROM pdbt_rate
                    WHERE state = ? AND billing_period >= ? AND billing_period <= ?
                """
                cursor.execute(query, (state, start_month, end_month))
                result = cursor.fetchall()
            if result:
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in result]
            return None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None