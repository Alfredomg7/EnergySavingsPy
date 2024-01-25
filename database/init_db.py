from database.db_setup import setup_database

def initialize_database():
    db_path = 'data/SolarData.db'
    locations_csv = 'data/locations.csv'
    solar_hours_csv = 'data/solar_hours.csv'

    setup_database(db_path, locations_csv, solar_hours_csv)

initialize_database()