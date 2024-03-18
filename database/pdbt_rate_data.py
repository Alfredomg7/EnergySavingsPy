import sqlite3
from database.dao_interface import PdbtRateDAO
from utils.date_utils import calculate_start_month
import config

class PdbtRateData(PdbtRateDAO):
    def __init__(self, db_path=config.DATABASE_PATH):
        self.db_path = db_path

    def get_charges(self, region_id, end_year_month):
        start_year_month = calculate_start_month(end_year_month)
        columns =  ['billing_period', 'transmission', 'distribution', 'cenace', 'supplier', 'services', 'energy', 'capacity']
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                    SELECT {','.join(columns)}
                    FROM pdbt_rate
                    WHERE region_id = ? 
                    AND billing_period BETWEEN ? AND ?
                    ORDER BY SUBSTR(billing_period, 6, 7)
                """
                cursor.execute(query, (region_id, start_year_month, end_year_month))
                result = cursor.fetchall()
            if result:
                return [dict(zip(columns, row)) for row in result]
            return None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None