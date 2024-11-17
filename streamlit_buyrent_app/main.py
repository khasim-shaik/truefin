import streamlit as st
from financial_utils import get_summary
from forms import (
    create_input_forms, create_summary_df, 
    format_summary_df, display_sections, 
    validate_input
)

def calculate_buy_rent():
    data = create_input_forms()
    if validate_input(data['purchase_value'], data['down_payment']):
        display_sections()
        summary = get_summary(data)
        df_summary = create_summary_df(summary)
        df_summary = format_summary_df(df_summary)
        st.table(df_summary)

if __name__ == "__main__":
    calculate_buy_rent()

