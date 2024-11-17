def get_home_value_after_period(data):
    purchase_value = data['purchase_value']
    avg_appreciation_per_year = data['avg_appreciation_per_year'] / 100
    years_to_hold = data['years_to_hold']
    return purchase_value * ((1 + avg_appreciation_per_year) ** years_to_hold)

def get_property_tax_monthly(data):
    purchase_value = data['purchase_value']
    property_tax_rate = data['tax_rate']
    return (property_tax_rate / 100 * purchase_value) / 12

def get_total_tax_paid(data):
    purchase_value = data['purchase_value']
    avg_appreciation_per_year = data['avg_appreciation_per_year'] / 100
    years_to_hold = data['years_to_hold']
    tax_rate = data['tax_rate'] / 100
    return sum([purchase_value * tax_rate * ((1 + avg_appreciation_per_year) ** i) 
               for i in range(years_to_hold)])

def get_insurance_monthly(data):
    purchase_value = data['purchase_value']
    return (purchase_value / 1000 * 3.5) / 12

def get_hoa_monthly(data):
    return data['hoa_payment']

def get_total_hoa_paid(data):
    years_to_hold = data['years_to_hold']
    hoa = data['hoa_payment']
    return sum([hoa * ((1 + 0.001) ** i) for i in range(years_to_hold)])

def get_maintenance_monthly(data):
    purchase_value = data['purchase_value']
    maintenance_rate = data['maintenance_rate'] / 100
    return purchase_value * maintenance_rate / 12

def get_annual_maintenance_cost(data):
    purchase_value = data['purchase_value']
    avg_appreciation_per_year = data['avg_appreciation_per_year'] / 100
    years_to_hold = data['years_to_hold']
    maintenance_rate = data['maintenance_rate'] / 100
    
    total_cost = 0
    for i in range(years_to_hold):
        yearly_cost = purchase_value * maintenance_rate * ((1 + avg_appreciation_per_year) ** i)
        if yearly_cost > 0:  # Sanity check
            total_cost += yearly_cost
    
    return total_cost if total_cost > 0 else 0

def get_selling_cost(data):
    future_value_of_home = get_home_value_after_period(data)
    return future_value_of_home * 0.08