import streamlit as st
import pandas as pd

def create_input_forms():
    st.title("Buy or Rent?")
    st.write("This app will help you decide whether to buy or rent a house.")

    home_price = st.number_input("Price of House", value=300000)
    down_payment = st.number_input("Down payment", value=320000)
    interest_rate = st.slider("Interest rate (%)", min_value=1.0, max_value=10.0, value=6.0, step=0.1, format="%f")
    tax_rate = st.slider("Tax rate (%)", min_value=1.0, max_value=5.0, value=1.0, step=0.1, format="%f")
    maintenance_rate = st.slider("Maintenance rate (%)", min_value=1.0, max_value=5.0, value=1.0, step=0.1, format="%f")
    pmi_rate = st.slider("PMI rate (%)", min_value=1.0, max_value=5.0, value=1.0, step=0.1, format="%f")
    insurance_rate = st.slider("Insurance rate (%)", min_value=1.0, max_value=5.0, value=1.0, step=0.1, format="%f")
    years_to_hold = st.number_input("Years to hold", value=30)
    rental_income = st.number_input("Rental income", value=1000)
    hoa_payment = st.number_input("HOA payment", value=100)
    avg_appreciation_per_year = st.slider("Average appreciation per year (%)", min_value=1, max_value=10, value=3, step=1, format="%f")
    rent_cost = st.slider("Rent cost", min_value=500, max_value=5000, value=1900, step=100, format="%d")

    return {
        'purchase_value': home_price,
        'down_payment': down_payment,
        'interest_rate': interest_rate,
        'years_to_hold': years_to_hold,
        'rental_income': rental_income,
        'tax_rate': tax_rate,
        'maintenance_rate': maintenance_rate,
        'pmi_rate': pmi_rate,
        'insurance_rate': insurance_rate,
        'hoa_payment': hoa_payment,
        'avg_appreciation_per_year': avg_appreciation_per_year,
        'rent_cost': rent_cost
    }

def create_summary_df(summary):
    df = pd.DataFrame(summary, index=[0])
    df = df.T.reset_index()
    df.columns = ['Metric', 'Value']
    return df

def format_summary_df(df):
    metrics_order = [
        'future_value_of_home',
        'monthly_payment',
        'property_tax',
        'pmi',
        'total_pmi_paid_in_owning',
        'monthly_net_cost_of_owning',
        'total_tax_paid_in_owning',
        'total_maintenance_cost_in_owning',
        'selling_cost',
        'total_money_spent',
        'total_money_gained',
        'total_principal_paid_in_owning',
        'total_interest_paid_in_owning',
        'mortgage_amount_remaining',
        'total_rent_earned_in_ownership',
        'sales_proceeds',
        'net_gain_or_loss',
        'net_gain_or_loss_present_value',
        'maintenance',
        'insurance',
        'hoa'
    ]
    
    df = df.set_index('Metric').reindex(metrics_order)
    
    # Debug print before formatting
    print("Debug - Before formatting:")
    print(df.loc['total_maintenance_cost_in_owning'])
    
    df['Value'] = df['Value'].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else "$0.00")
    
    # Debug print after formatting
    print("Debug - After formatting:")
    print(df.loc['total_maintenance_cost_in_owning'])
    
    return df

def display_sections():
    sections = ["Results", "Cost of ownership", "Cost of renting", "Summary"]
    for section in sections:
        st.subheader(section)

def validate_input(home_price, down_payment):
    if down_payment > home_price:
        st.error("Down payment cannot be greater than home price.")
        return False
    return True