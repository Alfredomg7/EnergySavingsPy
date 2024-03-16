class Rate:
    IVA_RATE = 1.08

    def __init__(self, region_id, end_month):
        self._region_id = region_id
        self._end_month = end_month
        self._charges = None
        self._fix_charge = None

    def _validate_charges(self):
        if not self._charges:
            raise ValueError("Charges data is not available")
        
        if not isinstance(self._charges, list):
            raise ValueError("Charges data must be a list")

        if len(self._charges) != 12:
            raise ValueError("Charges data list must contain 12 items")

        if not all(isinstance(charge, dict) for charge in self._charges):
            raise ValueError("Each item in charges data must be a dictionary")
        
    def _validate_monthly_consumption(self, value):

        if not isinstance(value, list):
            raise ValueError("monthly_consumption must be a list")
        
        if len(value) != 12:
            raise ValueError("monthly_consumption list must contain 12 items")
        
        if not all(item >= 0 for item in value):
            raise ValueError("All items in monthly_consumption must be positive numbers")
        
        return value
    
    @property
    def fix_charge(self):
        return self._fix_charge
        
    def calculate_monthly_payments(self, monthly_consumption):
        self._validate_monthly_consumption(monthly_consumption)

        return [self._calculate_payment(charge, consumption) for charge, consumption in zip(self._charges, monthly_consumption)]
    
    def _calculate_fix_charge(self):
        raise NotImplementedError("Subclasses must implement this method")
        
    def _calculate_payment(self, charge, consumption):
        raise NotImplementedError("Subclasses must implement this method")