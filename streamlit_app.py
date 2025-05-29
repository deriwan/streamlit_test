import streamlit as st
import requests

# Set the app title
st.title('🌍 Currency Exchange Rate Viewer')

# Add a welcome message
st.write('Welcome to the global exchange rate app!')

# Let user input a custom message
custom_message = st.text_input('Enter a custom message:', 'Hello, Streamlit!')
st.write('Customized Message:', custom_message)

# Get list of all supported currencies (using the same API)
symbol_response = requests.get('https://api.vatcomply.com/currencies')
if symbol_response.status_code == 200:
    currencies = symbol_response.json()
    currency_codes = sorted(currencies.keys())

    # Let user select a base currency
    base_currency = st.selectbox('Select base currency:', currency_codes, index=currency_codes.index('MYR'))

    # Call exchange rate API with selected base currency
    rate_response = requests.get(f'https://api.vatcomply.com/rates?base={base_currency}')
    if rate_response.status_code == 200:
        data = rate_response.json()
        rates = data.get('rates', {})

        # Let user pick a target currency to display specific exchange rate
        target_currency = st.selectbox('Select target currency to view rate:', currency_codes)

        # Display exchange rate
        if target_currency in rates:
            rate = rates[target_currency]
            st.success(f"1 {base_currency} = {rate} {target_currency}")
        
        # Optional: Show all exchange rates
        with st.expander("See all exchange rates"):
            st.json(rates)
    else:
        st.error(f"Exchange rate API failed: {rate_response.status_code}")
else:
    st.error(f"Currency list API failed: {symbol_response.status_code}")


