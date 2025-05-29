import streamlit as st
import requests

# Set the app title
st.title('🌍 Currency Exchange Rate Viewer')

# Add a welcome message
st.write('Welcome to the global exchange rate app!')

# Custom message input
custom_message = st.text_input('Enter a custom message:', 'Hello, Streamlit!')
st.write('Customized Message:', custom_message)

# Fetch available currencies
symbol_response = requests.get('https://api.vatcomply.com/currencies')
if symbol_response.status_code == 200:
    currencies = symbol_response.json()
    currency_codes = sorted(currencies.keys())

    # User selects base currency from dropdown
    base_currency = st.selectbox('Select base currency:', currency_codes, index=currency_codes.index('MYR'))

    # User selects target currency from dropdown
    target_currency = st.selectbox('Select target currency:', currency_codes, index=currency_codes.index('USD'))

    # Fetch exchange rate data
    rate_response = requests.get(f'https://api.vatcomply.com/rates?base={base_currency}')
    if rate_response.status_code == 200:
        data = rate_response.json()
        rates = data.get('rates', {})

        # Show the specific exchange rate
        if target_currency in rates:
            rate = rates[target_currency]
            st.success(f"💱 1 {base_currency} = {rate} {target_currency}")
        
        # Optional: Show all rates in an expandable box
        with st.expander("🔍 See all exchange rates"):
            st.json(rates)
    else:
        st.error(f"Exchange rate API failed with status code: {rate_response.status_code}")
else:
    st.error(f"Currency list API failed with status code: {symbol_response.status_code}")

 

