import streamlit as st  # type: ignore
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
import yfinance as yf  # type: ignore
import time  # For adding delay in retries
import plotly.graph_objects as go  # type: ignore
from datetime import datetime  # For date handling
from data_ingestion import INDICES  # Assuming INDICES is a dictionary containing stock data

# Function to get current stock price with error handling and retry mechanism
def get_stock_price(stock, retries=3, delay=2):
    """Fetch the current stock price with retries and error handling."""
    for attempt in range(retries):
        try:
            stock_data = yf.download(stock, period="1d", interval="1m")
            if not stock_data.empty:
                return stock_data['Close'].iloc[-1]
            else:
                st.error(f"No data available for {stock}.")
                return None
        except Exception as e:
            st.warning(f"Attempt {attempt + 1} to fetch data for {stock} failed: {e}")
            time.sleep(delay)  # Wait before retrying
    st.error(f"Failed to fetch data for {stock} after {retries} attempts.")
    return None

# Function to calculate historical volatility
def calculate_historical_volatility(price_data, window=30):
    """Calculate historical volatility based on closing prices."""
    log_returns = np.log(price_data / price_data.shift(1))
    rolling_volatility = log_returns.rolling(window=window).std() * np.sqrt(252)  # Annualize the volatility
    return rolling_volatility.iloc[-1]  # Return the most recent volatility value

# Function to calculate covariance and portfolio volatility
def calculate_covariance_and_volatility(volatilities, correlation_matrix, investments):
    """Calculate the covariance matrix and portfolio volatility."""
    n = len(volatilities)
    
    # Calculate covariance matrix
    covariance_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            covariance_matrix[i, j] = correlation_matrix[i, j] * volatilities[i] * volatilities[j]

    # Portfolio weights
    total_investment = sum(investments)
    weights = [inv / total_investment for inv in investments]

    # Portfolio volatility calculation
    portfolio_variance = sum(weights[i] * weights[j] * covariance_matrix[i, j] for i in range(n) for j in range(n))
    portfolio_volatility = np.sqrt(portfolio_variance)
    
    return covariance_matrix, portfolio_volatility

# Streamlit UI
st.title("Investment Portfolio Risk Assessment")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["Portfolio Management", "Risk Assessment", "Data Visualization"])

# Initialize session state for portfolio
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

# Currency selection
currency = st.sidebar.selectbox("Select Currency for Portfolio Calculations:", ("INR", "USD"))

# Get exchange rate (Placeholder function)
def get_exchange_rate():
    """Fetch the current exchange rate (Dummy implementation)."""
    return 82.5  # Example static value; replace with a dynamic fetch from a reliable API.

exchange_rate = get_exchange_rate()
if exchange_rate:
    st.sidebar.write(f"Current USD/INR exchange rate: {exchange_rate:.2f}")

if page == "Portfolio Management":
    st.subheader("Manage Your Portfolio")

    # Stock selection logic
    st.subheader("Select Stock Market Option")
    option = st.radio("Select an option:", ("Indian Stocks", "U.S. Stocks", "Manual Input"))

    # Predefined quantity options
    quantity_options = [5, 10, 50, 100, 1000]

    # Stock selection based on the chosen option
    if option == "Indian Stocks":
        index_choice = st.selectbox("Choose an index:", list(INDICES.keys())[:4])
        stock_options = list(INDICES[index_choice].values())
        selected_stocks = st.multiselect("Select stocks", stock_options)
        
        quantity = st.selectbox("Select quantity:", quantity_options)

        if st.button("Add to Portfolio"):
            for stock_symbol in selected_stocks:
                st.session_state.portfolio.append((stock_symbol, quantity, 'INR'))

    elif option == "U.S. Stocks":
        index_choice = st.selectbox("Choose a U.S. index:", list(INDICES.keys())[4:6])
        stock_options = list(INDICES[index_choice].values())
        selected_stocks = st.multiselect("Select stocks", stock_options)
        
        quantity = st.selectbox("Select quantity:", quantity_options)

        if st.button("Add to Portfolio"):
            for stock_symbol in selected_stocks:
                st.session_state.portfolio.append((stock_symbol, quantity, 'USD'))

    elif option == "Manual Input":
        stock_symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, MSFT):")
        if stock_symbol:
            quantity = st.selectbox("Select quantity:", quantity_options)
            if st.button("Add to Portfolio"):
                st.session_state.portfolio.append((stock_symbol, quantity, 'USD' if 'US' in stock_symbol else 'INR'))

    # Show the user's portfolio
    if st.session_state.portfolio:
        st.write("Your Portfolio:")
        total_value = 0
        investments = []  # List to store investment amounts
        volatilities = []  # List to store asset volatilities

        for stock, qty, stock_currency in st.session_state.portfolio:
            stock_price = get_stock_price(stock)
            if stock_price is not None:
                if currency == 'INR' and stock_currency == 'USD':
                    stock_price *= exchange_rate
                elif currency == 'USD' and stock_currency == 'INR':
                    stock_price /= exchange_rate
                
                stock_total = stock_price * qty
                total_value += stock_total
                investments.append(stock_total)  # Append investment value
                # Calculate and store historical volatility
                historical_volatility = calculate_historical_volatility(yf.download(stock, period="1y")['Close'])
                volatilities.append(historical_volatility)
                st.write(f"{stock}: {qty} shares @ {currency} {stock_price:.2f} = {currency} {stock_total:.2f} (Volatility: {historical_volatility:.4f})")
            else:
                st.write(f"{stock}: {qty} shares - Price data unavailable.")

        st.write(f"Total Portfolio Value: {currency} {total_value:.2f}")

        # Portfolio editing functionality
        if st.button("Edit Portfolio"):
            stock_to_remove = st.selectbox("Select stock to remove:", [s[0] for s in st.session_state.portfolio])
            st.session_state.portfolio = [s for s in st.session_state.portfolio if s[0] != stock_to_remove]
            st.success(f"Removed {stock_to_remove} from portfolio.")

if page == "Risk Assessment":
    st.subheader("Risk Assessment")

    # Initialize volatilities and investments in case the portfolio is empty
    volatilities = []
    investments = []

    # Check if the portfolio has assets
    if len(st.session_state.portfolio) > 1:
        correlation_matrix = np.random.rand(len(st.session_state.portfolio), len(st.session_state.portfolio))  # Random correlation values
        correlation_matrix = (correlation_matrix + correlation_matrix.T) / 2  # Make it symmetric
        np.fill_diagonal(correlation_matrix, 1)  # Fill diagonal with 1s

        # Populate volatilities and investments from the portfolio
        for stock, qty, stock_currency in st.session_state.portfolio:
            stock_price = get_stock_price(stock)
            if stock_price is not None:
                if currency == 'INR' and stock_currency == 'USD':
                    stock_price *= exchange_rate
                elif currency == 'USD' and stock_currency == 'INR':
                    stock_price /= exchange_rate
                
                # Calculate and store historical volatility
                historical_volatility = calculate_historical_volatility(yf.download(stock, period="1y")['Close'])
                volatilities.append(historical_volatility)
                investments.append(stock_price * qty)

        if st.button("Calculate Covariance and Portfolio Volatility"):
            covariance_matrix, portfolio_volatility = calculate_covariance_and_volatility(
                volatilities, correlation_matrix, investments
            )
            st.write("Covariance Matrix:")
            st.write(covariance_matrix)
            st.write(f"Portfolio Volatility: {portfolio_volatility:.4f}")

    else:
        st.warning("Please add more than one asset to calculate risk metrics.")

    # Calculate and display VaR (Placeholder function)
    if st.button("Calculate VaR (Value at Risk)"):
        if investments:
            VaR = np.percentile(investments, 5)  # Example implementation
            st.write(f"Value at Risk (5%): {VaR:.2f}")

if page == "Data Visualization":
    st.subheader("Visualize Your Data")
    
    # Show the performance of stocks in the portfolio
    start_date = st.date_input("Start Date", datetime.now())
    end_date = st.date_input("End Date", datetime.now())
    
    if st.button("Show Stock Performance"):
        for stock, qty, stock_currency in st.session_state.portfolio:
            stock_data = yf.download(stock, start=start_date, end=end_date)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name=stock))
            st.plotly_chart(fig)

# Additional enhancements, styling, and functionality can be added as needed.
