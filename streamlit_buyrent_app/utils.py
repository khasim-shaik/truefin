import pandas as pd


def get_home_value_after_period(data):
    purchase_value = data['purchase_value']
    avg_appreciation_per_year = data['avg_appreciation_per_year'] / 100
    years_to_hold = data['years_to_hold']

    future_value_of_home = purchase_value * ((1 + avg_appreciation_per_year) ** years_to_hold)
    return future_value_of_home

# create a new function to calculate the monthly payment. Assume that the monthly payment is paid monthly. Use simple calculations to calculate the monthly payment.
def get_monthly_mortogage_payment(data):
    # get the values from the data dictionary
    purchase_value = data['purchase_value']
    down_payment = data['down_payment']
    interest_rate = data['interest_rate'] / 100
    mortogage_duration_in__years=30

    # calculate the monthly payment
    monthly_payment = (purchase_value - down_payment) * (interest_rate / 12) * ((1 + interest_rate / 12) ** (mortogage_duration_in__years * 12)) / (((1 + interest_rate / 12) ** (mortogage_duration_in__years * 12)) - 1)

    # return the monthly payment
    return monthly_payment



def calculate_amortization_schedule(data):
    # get the values from the data dictionary
    purchase_price = data['purchase_value']
    down_payment = data['down_payment']
    interest_rate = data['interest_rate'] / 100
    mortgage_duration_in_years = 30

    # Calculate the loan amount
    loan_amount = purchase_price - down_payment

    # Calculate the number of months in the mortgage term
    months = mortgage_duration_in_years * 12

    # Calculate the monthly interest rate
    monthly_interest_rate = interest_rate / 12

    # Calculate the monthly payment using the formula for a fixed-payment loan
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** (-months))

    # Create an empty DataFrame to hold the amortization schedule
    columns = ['Month', 'Payment', 'Interest', 'Principal', 'Balance', 'Cumulative Payment', 'Cumulative Principal', 'Cumulative Interest']
    schedule = pd.DataFrame(index=range(months+1), columns=columns)

    # Set the initial values in the DataFrame
    schedule.loc[0] = [0, 0, 0, 0, loan_amount, 0, 0, 0]

    # Calculate the interest, principal, and remaining balance for each month
    for i in range(1, months+1):
        # Calculate the interest for the current month
        interest = schedule.loc[i-1]['Balance'] * monthly_interest_rate

        # Calculate the principal for the current month
        principal = monthly_payment - interest

        # Calculate the remaining balance after the current month's payment
        balance = schedule.loc[i-1]['Balance'] - principal

        # Calculate the cumulative payment, principal, and interest
        cumulative_payment = schedule.loc[i-1]['Cumulative Payment'] + monthly_payment
        cumulative_principal = schedule.loc[i-1]['Cumulative Principal'] + principal
        cumulative_interest = schedule.loc[i-1]['Cumulative Interest'] + interest

        # Update the values in the DataFrame for the current month
        schedule.loc[i] = [i, monthly_payment, interest, principal, balance, cumulative_payment, cumulative_principal, cumulative_interest]

    # Convert the numeric columns to float
    schedule = schedule.astype(float)

    return schedule


# use the calculate_amortization_schedule function to calculate the total interest paid on the home during the period of ownership.
# the function should call the calculate_amortization_schedule function and return the total interest paid on the home during the period of ownership.
# total period of ownership is the number of years to hold the home.
def get_total_interest_and_equity_paid(data):
    # get the values from the data dictionary
    purchase_value = data['purchase_value']
    down_payment = data['down_payment']
    interest_rate = data['interest_rate'] / 100
    mortogage_duration_in__years=30
    years_to_hold = data['years_to_hold']

    # calculate the total interest paid
    schedule = calculate_amortization_schedule(data)

    #months held
    months_held = years_to_hold * 12

    #total interest paid in months held 
    total_interest_paid = sum(schedule.loc[0:months_held, 'Interest'])

    #total equity paid in months held
    total_equity_paid = sum(schedule.loc[0:months_held, 'Principal'])

    # return the total interest paid
    return total_interest_paid, total_equity_paid


# write a function that does the following:
# 1. Calcuate 20% of the purchase price. call it 20_percent_point
# 2. Caculate the financed amount by subtracting the down payment from the purchase price. call it financed_amount
# 3. Use amortization schedule to sum the column principal such that sum of principal is equal to 20% of the financed amount.
# 4. return the number of years it takes to pay off 20% of the financed amount.
def get_years_to_pay_off_20_percent(data):
    # get the values from the data dictionary
    purchase_value = data['purchase_value']
    down_payment = data['down_payment']
    interest_rate = data['interest_rate'] / 100
    mortogage_duration_in__years=30

    # calculate the number of years to pay off 20% of the financed amount
    schedule = calculate_amortization_schedule(data)

    #calculate 20% of the purchase price
    
    twenty_percent_point = (purchase_value * 0.2) - down_payment

    if twenty_percent_point < 0: # if the down payment is more than 20% of the purchase price, return 0
        return 0

    #calculate the financed amount
    financed_amount = purchase_value - down_payment

    #calculate the number of years to pay off 20% of the financed amount using the column cumulative principal in the amortization schedule
    years_to_pay_off_20_percent = schedule.loc[schedule['Cumulative Principal'] <= twenty_percent_point, 'Month'].count() / 12.0
   

    # return the number of years to pay off 20% of the financed amount
    return years_to_pay_off_20_percent

# create a function to calculate PMI. PMI is only required if the down payment is less than 20% of the purchase price.
# It is calculated as 0.75% of the purchase price. Assume that the PMI is paid monthly.

def get_pmi_monthly(data):
    # get the values from the data dictionary
    purchase_value = data['purchase_value']
    down_payment = data['down_payment']
    financed_amount = purchase_value - down_payment
    pmi_rate = data['pmi_rate']

    # calculate the PMI
    if down_payment < 0.2 * purchase_value:
        pmi = pmi_rate / 100 * financed_amount
    else:
        pmi = 0

    # return the PMI
    return pmi/12.0


# calculate the total PMI paid till the point years_to_pay_off_20_percent is reached.
def get_total_pmi_paid(data):
    # get the values from the data dictionary
    purchase_value = data['purchase_value']
    down_payment = data['down_payment']
    years_to_hold = data['years_to_hold']

    # calculate the total PMI paid
    schedule = calculate_amortization_schedule(data)

    #calculate the number of years to pay off 20% of the financed amount using the column cumulative principal in the amortization schedule
    years_to_pay_off_20_percent = get_years_to_pay_off_20_percent(data)

    #calculate the total PMI paid till the point years_to_pay_off_20_percent is reached
    total_pmi_paid = years_to_pay_off_20_percent * 12.0 * get_pmi_monthly(data)

    # return the total PMI paid
    return total_pmi_paid

# calcualate the total principal paid during the period of ownership.
# assume that the principal is paid monthly.
def get_total_principal_paid(data):
    # get the values from the data dictionary
    purchase_value = data['purchase_value']
    down_payment = data['down_payment']
    interest_rate = data['interest_rate'] / 100
    mortogage_duration_in__years=30
    years_to_hold = data['years_to_hold']

    # calculate the total principal paid
    schedule = calculate_amortization_schedule(data)

    #months held
    months_held = years_to_hold * 12

    #total principal paid in months held 
    total_principal_paid = sum(schedule.loc[0:months_held, 'Principal'])

    # return the total principal paid
    return total_principal_paid

# calculate the total interest paid on the home during the period of ownership.
# assume that the interest is paid monthly.
def get_total_interest_paid(data):
    # get the values from the data dictionary
    purchase_value = data['purchase_value']
    down_payment = data['down_payment']
    interest_rate = data['interest_rate'] / 100
    mortogage_duration_in__years=30
    years_to_hold = data['years_to_hold']

    # calculate the total interest paid
    schedule = calculate_amortization_schedule(data)

    #months held
    months_held = years_to_hold * 12

    #total interest paid in months held 
    total_interest_paid = sum(schedule.loc[0:months_held, 'Interest'])

    # return the total interest paid
    return total_interest_paid




# create a function to calculate the monthly property tax. Assume that the property tax is paid monthly.
def get_property_tax_monthly(data):
    # get the values from the data dictionary
    purchase_value = data['purchase_value']
    # let's assume that the property tax rate is 1%
    property_tax_rate = data['property_tax_rate']

    # calculate the monthly property tax
    property_tax = property_tax_rate / 100 * purchase_value

    # return the monthly property tax
    return property_tax/12

# create a function to calculate the total tax paid on the home during the period of ownership.
# Assume the tax is 1% of the purchase price and increases by the average appreciation rate per year.
def get_total_tax_paid(data):
    # get the values from the data dictionary
    purchase_value = data['purchase_value']
    avg_appreciation_per_year = data['avg_appreciation_per_year'] / 100
    years_to_hold = data['years_to_hold']
    tax_rate = data['property_tax_rate'] / 100
    total_tax_paid = sum([ purchase_value * tax_rate * ((1 + avg_appreciation_per_year) ** i) for i in range(years_to_hold)])

    # return the total tax paid
    return total_tax_paid

# create a function to calculate the monthly insurance. Assume that the insurance is paid monthly.
# https://www.policygenius.com/homeowners-insurance/homeowners-insurance-calculator/#:~:text=What%20is%20the%20formula%20to,policy%20that%20costs%20roughly%20%241%2C400.
# You can calculate the approximate cost of homeowners insurance by dividing the value of your home by $1,000 and then multiplying the result by $3.50. For example, a home valued at $400,000 would have a home insurance policy that costs roughly $1,400.
def get_insurance_monthly(data):
    # get the values from the data dictionary
    purchase_value = data['purchase_value']

    # calculate the monthly insurance
    insurance = (purchase_value / 1000 * 3.5)/12

    # return the monthly insurance
    return insurance


# create a function to calculate the monthly HOA. Assume that the HOA is paid monthly.
def get_hoa_monthly(data):
    # get the values from the data dictionary
    hoa = data['hoa_payment']

    # return the monthly HOA
    return hoa

# claculate the total HOA paid during the period of ownership.
# assume that the HOA is paid monthly. Assume HOA increases by 0.1% per year.
def get_total_hoa_paid(data):
    # get the values from the data dictionary
    years_to_hold = data['years_to_hold']
    hoa = data['hoa_payment']

    total_hoa_paid = sum([ hoa * ((1 + 0.001) ** i) for i in range(years_to_hold)])

    # return the total HOA paid
    return total_hoa_paid

# create a function to calculate the monthly maintenance. Assume that the maintenance is paid monthly.
def get_maintenance_monthly(data):
    # get the values from the data dictionary
    purchase_value = data['purchase_value']
    maintaince_rate = data['maintaince_rate']/100
    # assuming 0.5% of total purchase value is spent on maintenance per year
    maintenance = purchase_value * maintaince_rate / 12

    # return the monthly maintenance
    return maintenance

# create a function to get total annual cost of maintainence of a home.
# Assume the annual maintenance cost is 0.5% of the present value of the home
def get_annual_maintenance_cost(data):
    # get the values from the data dictionary
    purchase_value = data['purchase_value']
    avg_appreciation_per_year = data['avg_appreciation_per_year'] / 100
    years_to_hold = data['years_to_hold']
    maintaince_rate = data['maintaince_rate']/100
    total_cost_of_maintainence= sum([ purchase_value*maintaince_rate * ((1 + avg_appreciation_per_year/100) ** i) for i in range(years_to_hold)])

    # return the annual maintenance cost
    return total_cost_of_maintainence



# create a function to calcualate the total monthly cost of owning a home. Use the functions you created above to calculate the monthly payment, PMI, property tax, insurance, HOA, maintenance, and utilities.
def get_monthly_cost_of_owning(data):
    # get the values from the data dictionary
    monthly_payment = get_monthly_mortogage_payment(data)
    pmi = get_pmi_monthly(data)
    property_tax = get_property_tax_monthly(data)
    insurance = get_insurance_monthly(data)
    hoa = get_hoa_monthly(data)
    maintenance = get_maintenance_monthly(data)

    # calculate the total monthly cost of owning a home
    total_monthly_cost_of_owning = monthly_payment + pmi + property_tax + insurance + hoa + maintenance

    results_cost_of_ownership = {
        'monthly_payment': monthly_payment,
        'pmi': pmi,
        'property_tax': property_tax,
        'insurance': insurance,
        'hoa': hoa,
        'maintenance': maintenance,
        'total_monthly_cost_of_owning': total_monthly_cost_of_owning
    }

    # return the total monthly cost of owning a home
    return results_cost_of_ownership 

# create a function to calculate the income generated by rental income. Assume that the rental income is paid monthly.
def get_monthly_rental_income(data):
    # get the values from the data dictionary
    monthly_rental_income = data['rental_income']

    # return the monthly rental income
    return monthly_rental_income

# create a function to calculate the total rental income generated during the period of ownership.
# Assume that the rental income is paid monthly. Assume that the rental income increases by 2% per year.
def get_total_rental_income(data):
    # get the values from the data dictionary
    years_to_hold = data['years_to_hold']
    monthly_rental_income = data['rental_income']

    total_rental_income = sum([ (monthly_rental_income*12) * ((1 + 0.02) ** i) for i in range(years_to_hold)])

    # return the total rental income
    return total_rental_income


# create a function to calculate the net payment. Since a part of the home can be rented to generate income, the net payment is the total monthly cost of owning a home minus the monthly rental income.
def get_net_payment(data):
    # get the values from the data dictionary
    total_monthly_cost_of_owning = get_monthly_cost_of_owning(data)['total_monthly_cost_of_owning']
    monthly_rental_income = get_monthly_rental_income(data)

    # calculate the net payment
    net_payment = total_monthly_cost_of_owning - monthly_rental_income

    # return the net payment
    return net_payment


# create a function to calculate the total monthly cost of renting a home. Assume that the rent is paid monthly. Assume that the rent increases by 2% per year.
def get_total_cost_of_renting(data):
    # get the values from the data dictionary
    rent = data['rent_cost']
    years_to_hold = data['years_to_hold']

    # calculate the total money spent on renting a home. Assuming the rent increases by 2% per year. and the occupant
    # stays for the number of years specified in the data dictionary.
    total_cost_of_renting= sum([(rent*12) * ((1 + 2/100) ** i) for i in range(years_to_hold)])


    # return the total monthly cost of renting a home
    return total_cost_of_renting


# get the selling cost of the home after the specified number of years. Assume selliing cost is 
# equal to 8% of the future value of the home

def get_selling_cost(data):
    # get the values from the data dictionary
    future_value_of_home = get_home_value_after_period(data)
    selling_cost = future_value_of_home * 0.08

    # return the selling cost
    return selling_cost

#calculate the mortgage amount remaining after the specified number of years

def get_mortogage_amount_remianing(data,total_principal_paid_in_owning):
    
    purchase_price = data['purchase_value']
    down_payment = data['down_payment']
    loan_amount = purchase_price - down_payment
    mortogage_amount_remaining= loan_amount - total_principal_paid_in_owning
    return mortogage_amount_remaining

# create a function to calculate the net present value of a given amount of money accouting for inflation
# Assume that the inflation rate is 3% per year.
def get_net_present_value(data, total_money_gained, total_money_spent):
    # get the values from the data dictionary
    years_to_hold = data['years_to_hold']
    inflation_rate = 3 / 100

    # present value of the money gained
    present_value_of_money_gained = total_money_gained/((1 + inflation_rate) ** years_to_hold)

    # present value of the money spent
    present_value_of_money_spent = total_money_spent/((1 + inflation_rate) ** years_to_hold)

    # net present value
    net_present_value = present_value_of_money_gained - present_value_of_money_spent - data['down_payment']

    # return the net present value
    return net_present_value

def get_summary(data):
    # get the values from the data dictionary
    future_value_of_home = get_home_value_after_period(data)
    total_monthly_cost_of_owning = get_monthly_cost_of_owning(data)
    monthly_net_cost_of_owning = get_net_payment(data)

    # annual numbers 
    total_hoa_cost_in_owning = get_total_hoa_paid(data)
    total_maintaince_cost_in_owning = get_annual_maintenance_cost(data)
    total_tax_paid_in_owning = get_total_tax_paid(data)
    total_principal_paid_in_owning = get_total_principal_paid(data)
    total_interest_paid_in_owning = get_total_interest_paid(data)
    total_pmi_paid_in_owning = get_total_pmi_paid(data)
    total_rent_earned_in_ownership = get_total_rental_income(data)

    # get the selling cost of the home after the specified number of years. Assume selliing cost is
    # equal to 8% of the future value of the home
    selling_cost=get_selling_cost(data)
    sales_proceeds = future_value_of_home - selling_cost

    # however, the selling cost is not the only cost. The mortgage amount remaining after the specified number of years is also a cost.
    #calculate the mortgage amount remaining after the specified number of years
    mortgage_amount_remaining = get_mortogage_amount_remianing(data,total_principal_paid_in_owning)

    # let's calculate the total amount of money that left your wallet till the end of the specified number of years
    total_money_spent = total_maintaince_cost_in_owning + total_tax_paid_in_owning + total_hoa_cost_in_owning + \
                        total_interest_paid_in_owning + total_principal_paid_in_owning + total_pmi_paid_in_owning +\
                        selling_cost + mortgage_amount_remaining
    
    # now let's get your income 
    total_money_gained = sales_proceeds + total_rent_earned_in_ownership 

    

    # now let's calculate the net gain or loss
    net_gain_or_loss = total_money_gained - total_money_spent - data['down_payment']

    # however, this is not the net gain or loss. We need to account for inflation.
    # Assume that the inflation rate is 3% per year.
    net_gain_or_loss_present_value = get_net_present_value(data, total_money_gained,total_money_spent)



    # what if you rented the home instead of owning it? How much money would you have paid in rent? 
    total_cost_of_renting = get_total_cost_of_renting(data)

    # create a dictionary with the above information
    summary = {
        'future_value_of_home': future_value_of_home,
        'total_cost_of_renting': total_cost_of_renting,
        'monthly_net_cost_of_owning': monthly_net_cost_of_owning,
        'total_maintaince_cost_in_owning': total_maintaince_cost_in_owning,
        'total_tax_paid_in_owning': total_tax_paid_in_owning,
        'total_principal_paid_in_owning': total_principal_paid_in_owning,
        'total_interest_paid_in_owning': total_interest_paid_in_owning,
        'total_pmi_paid_in_owning': total_pmi_paid_in_owning,
        'selling_cost': selling_cost,
        'mortgage_amount_remaining': mortgage_amount_remaining,
        'total_money_spent': total_money_spent,
        'sales_proceeds': sales_proceeds,
        'total_rent_earned_in_ownership': total_rent_earned_in_ownership,
        'total_money_gained': total_money_gained,
        'net_gain_or_loss': net_gain_or_loss,
        'total_hoa_cost_in_owning': total_hoa_cost_in_owning,
        'net_gain_or_loss': net_gain_or_loss,
        'net_gain_or_loss_present_value': net_gain_or_loss_present_value,
        'years_for_20_percent':get_years_to_pay_off_20_percent(data)
    }

    summary.update(total_monthly_cost_of_owning)



    # return the dictionary
    #round all numbers to 0 decimal places in the summary. If any number is a float, convert it to an integer. if any value in 
    # the dictionary is non-numeric then skip it.
    for key, value in summary.items():
        if isinstance(value, float):
            summary[key] = round(value)
        elif isinstance(value, int):
            summary[key] = int(value)
        else:
            continue
    
    return summary





