import streamlit as st
from utils.financials import calculate_buy_rent, validate_input
from components.forms import user_input_form

st.title("Buy or Rent?")
st.write("This app will help you decide whether to buy or rent a house.")

home_price, down_payment, interest_rate, tax_rate, maintenance_rate, pmi_rate, insurance_rate, years_to_hold, rental_income, hoa_payment, avg_appreciation_per_year, rent_cost = user_input_form()

if validate_input(home_price, down_payment):
    calculate_buy_rent(home_price, down_payment, interest_rate, tax_rate, maintenance_rate, pmi_rate, insurance_rate, years_to_hold, rental_income, hoa_payment, avg_appreciation_per_year, rent_cost)
