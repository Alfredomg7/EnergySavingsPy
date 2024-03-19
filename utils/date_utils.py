from datetime import datetime
from dateutil.relativedelta import relativedelta

def calculate_start_month(end_month):
    end_month_datetime = datetime.strptime(end_month, '%Y-%m')
    start_month_datetime = end_month_datetime - relativedelta(months=11)
    start_month = start_month_datetime.strftime('%Y-%m')
    return start_month

def format_month(year, month):
    year_month = f"{year}-{month:02d}"
    return year_month

def extract_month(year_month):
    month_datetime = datetime.strptime(year_month, '%Y-%m')
    month = month_datetime.month
    return month
    
def extract_year(year_month):
    year_datetime = datetime.strptime(year_month, '%Y-%m')
    year = year_datetime.year
    return year

def generate_months(start_month):
    # Summer/Winter charges applies during 6 months
    season_duration = 6
    months = []
    
    for i in range(season_duration):
        month = (start_month + i) % 12 or 12 # Handles the case when the month is 12 (december) or greater
        months.append(month)
    
    return months

def get_winter_start_month(summer_start_month):
    season_duration = 6
    # Winter season start the next month after the summer season ends
    winter_start_month = (summer_start_month + season_duration) % 12 or 12
    return winter_start_month
