import pandas as pd

def get_monthly_mortgage_payment(data):
    purchase_value = data['purchase_value']
    down_payment = data['down_payment']
    interest_rate = data['interest_rate'] / 100
    mortgage_duration_in_years = 30

    monthly_payment = (purchase_value - down_payment) * (interest_rate / 12) * \
                     ((1 + interest_rate / 12) ** (mortgage_duration_in_years * 12)) / \
                     (((1 + interest_rate / 12) ** (mortgage_duration_in_years * 12)) - 1)
    return monthly_payment

def calculate_amortization_schedule(data):
    purchase_price = data['purchase_value']
    down_payment = data['down_payment']
    interest_rate = data['interest_rate'] / 100
    mortgage_duration_in_years = 30

    loan_amount = purchase_price - down_payment
    months = mortgage_duration_in_years * 12
    monthly_interest_rate = interest_rate / 12
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** (-months))

    columns = ['Month', 'Payment', 'Interest', 'Principal', 'Balance', 
              'Cumulative Payment', 'Cumulative Principal', 'Cumulative Interest']
    schedule = pd.DataFrame(index=range(months+1), columns=columns)
    schedule.loc[0] = [0, 0, 0, 0, loan_amount, 0, 0, 0]

    for i in range(1, months+1):
        interest = schedule.loc[i-1]['Balance'] * monthly_interest_rate
        principal = monthly_payment - interest
        balance = schedule.loc[i-1]['Balance'] - principal
        cumulative_payment = schedule.loc[i-1]['Cumulative Payment'] + monthly_payment
        cumulative_principal = schedule.loc[i-1]['Cumulative Principal'] + principal
        cumulative_interest = schedule.loc[i-1]['Cumulative Interest'] + interest

        schedule.loc[i] = [i, monthly_payment, interest, principal, balance, 
                          cumulative_payment, cumulative_principal, cumulative_interest]

    return schedule.astype(float)

def get_years_to_pay_off_20_percent(data):
    purchase_value = data['purchase_value']
    down_payment = data['down_payment']
    
    twenty_percent_point = (purchase_value * 0.2) - down_payment
    if twenty_percent_point < 0:
        return 0

    schedule = calculate_amortization_schedule(data)
    years = schedule.loc[schedule['Cumulative Principal'] <= twenty_percent_point, 'Month'].count() / 12.0
    return years

def get_pmi_monthly(data):
    purchase_value = data['purchase_value']
    down_payment = data['down_payment']
    financed_amount = purchase_value - down_payment
    pmi_rate = data['pmi_rate']

    if down_payment < 0.2 * purchase_value:
        pmi = pmi_rate / 100 * financed_amount
    else:
        pmi = 0
    return pmi/12.0

def get_total_pmi_paid(data):
    years_to_pay_off_20_percent = get_years_to_pay_off_20_percent(data)
    total_pmi_paid = years_to_pay_off_20_percent * 12.0 * get_pmi_monthly(data)
    return total_pmi_paid

def get_total_principal_paid(data):
    years_to_hold = data['years_to_hold']
    schedule = calculate_amortization_schedule(data)
    months_held = years_to_hold * 12
    return sum(schedule.loc[0:months_held, 'Principal'])

def get_total_interest_paid(data):
    years_to_hold = data['years_to_hold']
    schedule = calculate_amortization_schedule(data)
    months_held = years_to_hold * 12
    return sum(schedule.loc[0:months_held, 'Interest'])

def get_mortgage_amount_remaining(data, total_principal_paid_in_owning):
    purchase_price = data['purchase_value']
    down_payment = data['down_payment']
    loan_amount = purchase_price - down_payment
    return loan_amount - total_principal_paid_in_owning 