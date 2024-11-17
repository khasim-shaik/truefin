from mortgage_utils import (
    get_monthly_mortgage_payment, get_total_principal_paid,
    get_total_interest_paid, get_total_pmi_paid,
    get_mortgage_amount_remaining, get_pmi_monthly,
    get_years_to_pay_off_20_percent
)
from property_utils import (
    get_home_value_after_period, get_property_tax_monthly,
    get_total_tax_paid, get_insurance_monthly,
    get_hoa_monthly, get_total_hoa_paid,
    get_maintenance_monthly, get_annual_maintenance_cost,
    get_selling_cost
)

def get_monthly_cost_of_owning(data):
    monthly_payment = get_monthly_mortgage_payment(data)
    pmi = get_pmi_monthly(data)
    property_tax = get_property_tax_monthly(data)
    insurance = get_insurance_monthly(data)
    hoa = get_hoa_monthly(data)
    maintenance = get_maintenance_monthly(data)

    total_monthly_cost = monthly_payment + pmi + property_tax + insurance + hoa + maintenance

    return {
        'monthly_payment': monthly_payment,
        'pmi': pmi,
        'property_tax': property_tax,
        'insurance': insurance,
        'hoa': hoa,
        'maintenance': maintenance,
        'total_monthly_cost_of_owning': total_monthly_cost
    }

def get_monthly_rental_income(data):
    return data['rental_income']

def get_total_rental_income(data):
    years_to_hold = data['years_to_hold']
    monthly_rental_income = data['rental_income']
    return sum([(monthly_rental_income*12) * ((1 + 0.02) ** i) 
               for i in range(years_to_hold)])

def get_net_payment(data):
    total_monthly_cost = get_monthly_cost_of_owning(data)['total_monthly_cost_of_owning']
    monthly_rental_income = get_monthly_rental_income(data)
    return total_monthly_cost - monthly_rental_income

def get_total_cost_of_renting(data):
    rent = data['rent_cost']
    years_to_hold = data['years_to_hold']
    return sum([(rent*12) * ((1 + 2/100) ** i) for i in range(years_to_hold)])

def get_net_present_value(data, total_money_gained, total_money_spent):
    years_to_hold = data['years_to_hold']
    inflation_rate = 3 / 100

    present_value_gained = total_money_gained/((1 + inflation_rate) ** years_to_hold)
    present_value_spent = total_money_spent/((1 + inflation_rate) ** years_to_hold)

    return present_value_gained - present_value_spent - data['down_payment']

def get_summary(data):
    future_value_of_home = get_home_value_after_period(data)
    monthly_costs = get_monthly_cost_of_owning(data)
    monthly_net_cost = get_net_payment(data)

    total_hoa_cost = get_total_hoa_paid(data)
    total_maintenance_cost = get_annual_maintenance_cost(data)
    print(f"Debug - Maintenance Cost Calculation:")
    print(f"Purchase Value: {data['purchase_value']}")
    print(f"Maintenance Rate: {data['maintenance_rate']}")
    print(f"Years to Hold: {data['years_to_hold']}")
    print(f"Appreciation Rate: {data['avg_appreciation_per_year']}")
    print(f"Calculated Maintenance Cost: {total_maintenance_cost}")
    total_tax_paid = get_total_tax_paid(data)
    total_principal_paid = get_total_principal_paid(data)
    total_interest_paid = get_total_interest_paid(data)
    total_pmi_paid = get_total_pmi_paid(data)
    total_rent_earned = get_total_rental_income(data)

    selling_cost = get_selling_cost(data)
    sales_proceeds = future_value_of_home - selling_cost
    mortgage_remaining = get_mortgage_amount_remaining(data, total_principal_paid)

    total_money_spent = (total_maintenance_cost + total_tax_paid + total_hoa_cost +
                        total_interest_paid + total_principal_paid + total_pmi_paid +
                        selling_cost + mortgage_remaining)
    
    total_money_gained = sales_proceeds + total_rent_earned
    net_gain_or_loss = total_money_gained - total_money_spent - data['down_payment']
    net_present_value = get_net_present_value(data, total_money_gained, total_money_spent)
    total_cost_of_renting = get_total_cost_of_renting(data)

    summary = {
        'future_value_of_home': future_value_of_home,
        'total_cost_of_renting': total_cost_of_renting,
        'monthly_net_cost_of_owning': monthly_net_cost,
        'total_maintenance_cost_in_owning': total_maintenance_cost,
        'total_tax_paid_in_owning': total_tax_paid,
        'total_principal_paid_in_owning': total_principal_paid,
        'total_interest_paid_in_owning': total_interest_paid,
        'total_pmi_paid_in_owning': total_pmi_paid,
        'selling_cost': selling_cost,
        'mortgage_amount_remaining': mortgage_remaining,
        'total_money_spent': total_money_spent,
        'sales_proceeds': sales_proceeds,
        'total_rent_earned_in_ownership': total_rent_earned,
        'total_money_gained': total_money_gained,
        'net_gain_or_loss': net_gain_or_loss,
        'total_hoa_cost_in_owning': total_hoa_cost,
        'net_gain_or_loss_present_value': net_present_value,
        'years_for_20_percent': get_years_to_pay_off_20_percent(data)
    }

    summary.update(monthly_costs)

    # Round all numeric values
    for key, value in summary.items():
        if isinstance(value, (float, int)):
            summary[key] = round(value)
    
    return summary 