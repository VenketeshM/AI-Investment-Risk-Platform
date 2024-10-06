import streamlit as st  # type: ignore
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
import yfinance as yf  # type: ignore
import time  # For adding delay in retries
import plotly.graph_objects as go  # type: ignore
from data_ingestion import INDICES  # Assuming INDICES is a dictionary containing stock data

# Function to get current stock price with error handling and retry mechanism
def get_stock_price(stock, retries=3, delay=2):
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

# Function to get the USD/INR exchange rate
def get_exchange_rate():
    try:
        exchange_data = yf.download('USDINR=X', period='1d', interval='1m')
        if not exchange_data.empty:
            return exchange_data['Close'].iloc[-1]
        else:
            st.error("No exchange rate data available.")
            return None
    except Exception as e:
        st.error(f"Error fetching exchange rate: {e}")
        return None

# Function to plot stock performance
def plot_stock_performance(stock, quantity):
    stock_data = yf.download(stock, period='1mo')  # Adjust period as needed
    stock_data['Total Value'] = stock_data['Close'] * quantity
    stock_data.reset_index(inplace=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Total Value'], mode='lines', name=stock))
    fig.update_layout(title=f'{stock} Performance Over the Last Month', xaxis_title='Date', yaxis_title='Total Value')
    return fig

# Define a function for portfolio weight visualization
def plot_portfolio_weights(portfolio):
    weights = [get_stock_price(stock) * qty for stock, qty, _ in portfolio]
    labels = [stock for stock, qty, _ in portfolio]

    fig = go.Figure(data=[go.Pie(labels=labels, values=weights, hole=0.3)])
    fig.update_layout(title="Portfolio Weights")
    return fig

# Define a function to calculate VaR using Monte Carlo simulation
def monte_carlo_var(portfolio, num_simulations=10000, confidence_level=0.95):
    returns = pd.DataFrame()

    for stock, qty, currency in portfolio:
        stock_data = yf.download(stock, period="1y")
        if stock_data.empty or 'Close' not in stock_data.columns:
            st.error(f"No historical data available for {stock}.")
            return None

        stock_returns = stock_data['Close'].pct_change().dropna() * qty
        returns[stock] = stock_returns

    portfolio_returns = returns.sum(axis=1)

    simulations = np.random.normal(portfolio_returns.mean(), portfolio_returns.std(), num_simulations)
    var = np.percentile(simulations, (1 - confidence_level) * 100)
    return var

# Function to perform a simple stress test
def stress_test(portfolio, market_crash_percentage=0.2):
    total_value_before_stress = 0
    stress_results = {}

    # Calculate the total value before the stress test
    for stock, qty, currency in portfolio:
        stock_price = get_stock_price(stock)
        if stock_price is not None:
            if currency == 'INR' and currency == 'USD':
                stock_price *= exchange_rate
            elif currency == 'USD' and currency == 'INR':
                stock_price /= exchange_rate
            
            total_value_before_stress += stock_price * qty
    
    # Simulate a market crash
    stress_value = total_value_before_stress * (1 - market_crash_percentage)
    stress_results["Market Crash (20% decline)"] = stress_value

    return stress_results

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

# Get exchange rate
exchange_rate = get_exchange_rate()
if exchange_rate:
    st.sidebar.write(f"Current USD/INR exchange rate: {exchange_rate:.2f}")

if page == "Portfolio Management":
    st.subheader("Manage Your Portfolio")

    # Stock selection logic
    st.subheader("Select Stock Market Option")
    option = st.radio("Select an option:", ("Indian Stocks", "U.S. Stocks", "Manual Input"))

    if option == "Indian Stocks":
        index_choice = st.selectbox("Choose an index:", list(INDICES.keys())[:4])
        stock_options = list(INDICES[index_choice].values())
        selected_stocks = st.multiselect("Select stocks", stock_options)
        
        # Predefined quantity options
        quantity_options = [5, 10, 50, 100, 1000]
        quantity = st.selectbox("Select quantity:", quantity_options)

        if st.button("Add to Portfolio"):
            for stock_symbol in selected_stocks:
                st.session_state.portfolio.append((stock_symbol, quantity, 'INR'))

    elif option == "U.S. Stocks":
        index_choice = st.selectbox("Choose a U.S. index:", list(INDICES.keys())[4:6])
        stock_options = list(INDICES[index_choice].values())
        selected_stocks = st.multiselect("Select stocks", stock_options)
        
        quantity_options = [5, 10, 50, 100, 1000]
        quantity = st.selectbox("Select quantity:", quantity_options)

        if st.button("Add to Portfolio"):
            for stock_symbol in selected_stocks:
                st.session_state.portfolio.append((stock_symbol, quantity, 'USD'))

    elif option == "Manual Input":
        stock_symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, MSFT):")
        if stock_symbol:
            quantity_options = [5, 10, 50, 100, 1000]
            quantity = st.selectbox("Select quantity:", quantity_options)
            if st.button("Add to Portfolio"):
                st.session_state.portfolio.append((stock_symbol, quantity, 'USD' if 'US' in stock_symbol else 'INR'))

    # Show the user's portfolio
    if st.session_state.portfolio:
        st.write("Your Portfolio:")
        total_value = 0
        for stock, qty, stock_currency in st.session_state.portfolio:
            stock_price = get_stock_price(stock)
            if stock_price is not None:
                if currency == 'INR' and stock_currency == 'USD':
                    stock_price *= exchange_rate
                elif currency == 'USD' and stock_currency == 'INR':
                    stock_price /= exchange_rate
                
                stock_total = stock_price * qty
                total_value += stock_total
                st.write(f"{stock}: {qty} shares @ {currency} {stock_price:.2f} = {currency} {stock_total:.2f}")
            else:
                st.write(f"{stock}: {qty} shares - Price data unavailable.")

        st.write(f"Total Portfolio Value: {currency} {total_value:.2f}")

if page == "Risk Assessment":
    st.subheader("Risk Assessment")

    # Calculate and display VaR
    if st.button("Calculate VaR"):
        var = monte_carlo_var(st.session_state.portfolio)
        if var is not None:
            st.write(f"Value at Risk (VaR) at 95% confidence level: {var:.2%}")

    # Perform and display stress tests
    if st.button("Run Stress Test"):
        stress_results = stress_test(st.session_state.portfolio)
        if stress_results:
            st.write("Stress Test Results:")
            for condition, value in stress_results.items():
                st.write(f"{condition}: {currency} {value:.2f}")

if page == "Data Visualization":
    st.subheader("Data Visualization")

    # Portfolio summary visualization
    if st.session_state.portfolio:
        weights_fig = plot_portfolio_weights(st.session_state.portfolio)
        st.plotly_chart(weights_fig)

        # Display stock performance for each stock in the portfolio
        for stock, qty, _ in st.session_state.portfolio:
            performance_fig = plot_stock_performance(stock, qty)
            st.plotly_chart(performance_fig)

# Quit button
if st.button("Quit"):
    st.write("Thank you for using the Investment Portfolio Risk Assessment tool. You can close the tab to exit.")
