from models.location import Location

class Rate:
    IVA_RATE = 1.08

    def __init__(self, location, end_year_month):
        self._location = self._validate_location(location)
        self._end_year_month = end_year_month
        self._charges = None

    def _validate_location(self, value):
        if not isinstance(value, Location):
            raise ValueError("The location object must be an instance of Location")
        return value

    def _validate_charges(self, value):
        if not value:
            raise ValueError("Charges data is not available")
        
        if not isinstance(value, list):
            raise ValueError("Charges data must be a list")

        if len(value) != 12:
            raise ValueError(f"Charges data list must contain data for 12 months")

        if not all(isinstance(item, dict) for item in value):
            raise ValueError("Each item in charges data must be a dictionary")

        return value
    
    def _validate_monthly_consumption(self, value):

        if not isinstance(value, list):
            raise ValueError("monthly_consumption must be a list")
        
        if len(value) != 12:
            raise ValueError("monthly_consumption list must contain 12 items")
        
        if not all(item >= 0 for item in value):
            raise ValueError("All items in monthly_consumption must be positive numbers")
        
        return value
        
    def calculate_monthly_payments(self, monthly_consumption):
        monthly_consumption = self._validate_monthly_consumption(monthly_consumption)

        return [self._calculate_payment(charge, consumption) for charge, consumption in zip(self._charges, monthly_consumption)]
        
    def _calculate_payment(self, charge, consumption):
        raise NotImplementedError("Subclasses must implement this method")