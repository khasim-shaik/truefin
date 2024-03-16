import streamlit as st

def user_input_form():
    with st.form("input_form"):
        home_price = st.number_input("Price of House", value=600000)
        down_payment = st.number_input("Down payment", value=320000)
        interest_rate = st.slider("Interest rate (%)", min_value=1.0, max_value=10.0, value=6.0, step=0.1, format="%f")
        tax_rate = st.slider("Tax rate (%)", min_value=1.0, max_value=5.0, value=1.0, step=0.1, format="%f")
        maintenance_rate = st.slider("Maintenance rate (%)", min_value=1.0, max_value=5.0, value=1.0, step=0.1, format="%f")
        pmi_rate = st.slider("PMI rate (%)", min_value=1.0, max_value=5.0, value=1.0, step=0.1, format="%f")
        years_to_hold = st.number_input("Years to hold", value=30)
        rental_income = st.number_input("Rental income", value=1000)
        hoa_payment = st.number_input("HOA payment", value=100)
        avg_appreciation_per_year = st.slider("Average appreciation per year (%)", min_value=1, max_value=10, value=3, step=1, format="%f")
        rent_cost = st.slider("Rent cost", min_value=500, max_value=5000, value=1900, step=100, format="%d")
        
        submitted = st.form_submit_button("Submit")
    
    
    return submitted,home_price, down_payment, interest_rate, tax_rate, maintenance_rate, pmi_rate, years_to_hold, rental_income, hoa_payment, avg_appreciation_per_year, rent_cost
