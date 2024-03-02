from datetime import datetime
from dateutil.relativedelta import relativedelta

def calculate_start_month(end_month):
    end_month_datetime = datetime.strptime(end_month, '%Y-%m')
    start_month_datetime = end_month_datetime - relativedelta(months=11)
    start_month = start_month_datetime.strftime('%Y-%m')
    return start_month

if __name__ == "__main__":
    start_month = calculate_start_month('2023-07')
    print(start_month)