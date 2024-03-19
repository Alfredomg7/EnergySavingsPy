import sqlite3
from database.dao_interface import ResidentialRatesDAO
from utils.date_utils import calculate_start_month, extract_month, extract_year, format_month
import config

class ResidentialRatesData(ResidentialRatesDAO):
    def __init__(self, db_path=config.DATABASE_PATH):
        self.db_path = db_path

    def _generate_year_months(self, season_months, end_year_month):
        start_year_month = calculate_start_month(end_year_month)
        year_months = []
        start_year = extract_year(start_year_month)
        start_month = extract_month(start_year_month)

        for month in season_months:
            year = start_year if month >= start_month else start_year + 1
            year_month = format_month(year, month)
            year_months.append(year_month)

        return year_months

    def _retrieve_charges(self, rate, year_months, table_name, columns):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                placeholders = ', '.join('?' for _ in year_months)
                query = f"""
                    SELECT {', '.join(columns)}
                    FROM {table_name}
                    WHERE rate = ?
                    AND billing_period IN ({placeholders})
                """
                cursor.execute(query, [rate] + year_months)
                result = cursor.fetchall()
            if result:
                return [dict(zip(columns, row)) for row in result]
            return None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    def get_summer_charges(self, rate, summer_months, end_year_month):
        year_months = self._generate_year_months(summer_months, end_year_month)
        columns = ['billing_period', 'basic', 'low_intermediate', 'high_intermediate', 'excess']
        return self._retrieve_charges(rate, year_months, 'residential_summer_rates', columns)

    def get_winter_charges(self, rate, winter_months, end_year_month):
        year_months = self._generate_year_months(winter_months, end_year_month)
        columns = ['basic', 'intermediate', 'excess']
        return self._retrieve_charges(rate, year_months, 'residential_winter_rates', columns)
