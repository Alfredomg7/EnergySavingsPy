from datetime import datetime
from dateutil.relativedelta import relativedelta
from calendar import monthrange

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

def generate_days_in_month(end_year_month):
    start_year_month = calculate_start_month(end_year_month)
    start_month = extract_month(start_year_month)
    start_year = extract_year(start_year_month)
    days_in_month = []
    for i in range(start_month, start_month + 12):
        month = (i - 1) % 12 + 1
        year = start_year + (i - 1) // 12
        days_in_month.append(monthrange(year, month)[1])
    return days_in_month