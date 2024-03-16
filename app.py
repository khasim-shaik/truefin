import streamlit as st
from utils.financials import calculate_buy_rent, validate_input
from components.forms import user_input_form

st.title("Buy or Rent?")
st.write("This app will help you to decide whether to buy or rent a house.")


submitted,home_price, down_payment, interest_rate, tax_rate, maintenance_rate, pmi_rate, years_to_hold, rental_income, hoa_payment, avg_appreciation_per_year, rent_cost = user_input_form()

if submitted:

    if validate_input(home_price, down_payment):
        
        results = calculate_buy_rent(purchase_value=home_price, down_payment=down_payment, \
                        interest_rate=interest_rate, tax_rate=tax_rate, maintenance_rate=maintenance_rate, \
                        pmi_rate=pmi_rate, years_to_hold=years_to_hold,\
                        rental_income=rental_income, hoa_payment=hoa_payment, \
                        avg_appreciation_per_year=avg_appreciation_per_year, rent_cost=rent_cost)
        st.write("### Results")
        st.table(results)