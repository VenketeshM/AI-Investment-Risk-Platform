import streamlit as st
import yfinance as yf

# Sample index data, replace with your actual index definitions


def fetch_stock_data(symbol):
    """Fetch stock data from Yahoo Finance."""
    try:
        stock = yf.Ticker(symbol)
        stock_info = stock.info
        data = stock.history(period="1d")  # Fetching the latest day's data
        if not data.empty:
            output = data.iloc[-1].to_dict()
            return {
                "Open": stock_info.get("open", "N/A"),
                "High": stock_info.get("high", "N/A"),
                "Low": stock_info.get("low", "N/A"),
                "Close": stock_info.get("previousClose", "N/A"),
                "Volume": stock_info.get("volume", "N/A"),
                "Dividends": stock_info.get("dividendRate", "N/A"),
                "Stock Splits": stock_info.get("lastSplitFactor", "N/A"),
            }
        else:
            return None
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {e}")
        return None

def fetch_financial_data(symbol):
    """Fetch income statement, balance sheet, and cash flow statement from Yahoo Finance."""
    try:
        stock = yf.Ticker(symbol)
        income_statement = stock.financials
        balance_sheet = stock.balance_sheet
        cash_flow = stock.cashflow
        
        return income_statement, balance_sheet, cash_flow
    except Exception as e:
        st.error(f"Error fetching financial data for {symbol}: {e}")
        return None, None, None

def format_to_crores(df):
    """Convert financial figures to crores and format the DataFrame."""
    if df is not None and not df.empty:
        df_crores = df / 10_000_000
        df_crores = df_crores.round(2)
        return df_crores
    else:
        return df

def calculate_metrics(income, balance, cash_flow):
    """Calculate financial metrics like ROE, ROC, EBITDA, etc."""
    metrics = {}
    
    try:
        if 'Net Income' in income.index and 'Total Equity' in balance.index:
            net_income = income.loc['Net Income'].iloc[0]
            shareholders_equity = balance.loc['Total Equity'].iloc[0]
            metrics['ROE (%)'] = (net_income / shareholders_equity) * 100
        
        if 'EBITDA' in income.index and 'Interest Expense' in income.index and 'Total Assets' in balance.index and 'Current Liabilities' in balance.index:
            net_income = income.loc['Net Income'].iloc[0]
            interest_expense = income.loc['Interest Expense'].iloc[0]
            total_assets = balance.loc['Total Assets'].iloc[0]
            current_liabilities = balance.loc['Current Liabilities'].iloc[0]
            metrics['ROC (%)'] = ((net_income + interest_expense) / (total_assets - current_liabilities)) * 100
        
        if 'EBITDA' in income.index:
            ebitda = income.loc['EBITDA'].iloc[0]
            metrics['EBITDA (Crores)'] = ebitda / 10_000_000
        
        if 'Total Debt' in balance.index and 'Total Equity' in balance.index:
            total_debt = balance.loc['Total Debt'].iloc[0]
            total_equity = balance.loc['Total Equity'].iloc[0]
            metrics['Debt to Equity Ratio'] = total_debt / total_equity
        
        if 'Net Income' in income.index and 'Total Revenue' in income.index:
            net_income = income.loc['Net Income'].iloc[0]
            total_revenue = income.loc['Total Revenue'].iloc[0]
            metrics['Net Profit Margin (%)'] = (net_income / total_revenue) * 100
        
        if 'Net Income' in income.index and 'Total Assets' in balance.index:
            net_income = income.loc['Net Income'].iloc[0]
            total_assets = balance.loc['Total Assets'].iloc[0]
            metrics['ROA (%)'] = (net_income / total_assets) * 100
        
        if 'Current Assets' in balance.index and 'Current Liabilities' in balance.index:
            current_assets = balance.loc['Current Assets'].iloc[0]
            current_liabilities = balance.loc['Current Liabilities'].iloc[0]
            metrics['Current Ratio'] = current_assets / current_liabilities
        
    except Exception as e:
        st.error(f"Error calculating metrics: {e}")
    
    return metrics

def display_financial_data(income, balance, cash_flow):
    """Display formatted financial data along with calculated metrics."""
    
    # Scrollable container for Income Statement
    st.subheader("Income Statement")
    with st.container():
        st.write('<div style="overflow-y: scroll; max-height: 400px;">', unsafe_allow_html=True)
        if income is not None and not income.empty:
            income_formatted = format_to_crores(income)
            st.dataframe(income_formatted)
        else:
            st.warning("No Income Statement data available.")
        st.write('</div>', unsafe_allow_html=True)

    # Scrollable container for Balance Sheet
    st.subheader("Balance Sheet")
    with st.container():
        st.write('<div style="overflow-y: scroll; max-height: 400px;">', unsafe_allow_html=True)
        if balance is not None and not balance.empty:
            balance_formatted = format_to_crores(balance)
            st.dataframe(balance_formatted)
        else:
            st.warning("No Balance Sheet data available.")
        st.write('</div>', unsafe_allow_html=True)

    # Scrollable container for Cash Flow Statement
    st.subheader("Cash Flow Statement")
    with st.container():
        st.write('<div style="overflow-y: scroll; max-height: 400px;">', unsafe_allow_html=True)
        if cash_flow is not None and not cash_flow.empty:
            cash_flow_formatted = format_to_crores(cash_flow)
            st.dataframe(cash_flow_formatted)
        else:
            st.warning("No Cash Flow Statement data available.")
        st.write('</div>', unsafe_allow_html=True)

    metrics = calculate_metrics(income, balance, cash_flow)
    if metrics:
        st.subheader("Financial Metrics")
        for metric, value in metrics.items():
            st.write(f"{metric}: {value:.2f}" if isinstance(value, float) else f"{metric}: {value}")
    else:
        st.warning("No financial metrics available.")

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(page_title="Stock and Financial Data Viewer", layout="wide")  # Set the layout to wide
    st.title("Stock and Financial Data Viewer")
    
    choice = st.selectbox("Select an option:", ["Indian Stocks", "U.S. Stocks", "Manual Input"])
    
    if choice == "Indian Stocks":
        selected_index = st.selectbox("Select an index:", list(INDICES.keys()))
        stock_options = list(INDICES[selected_index].items())
        stock_names = [f"{name} ({symbol})" for name, symbol in stock_options]
        stock_choice = st.selectbox("Select a stock:", stock_names)
        
        # Correctly extract the stock symbol
        stock_symbol = stock_choice.split('(')[-1].strip(')')  # Correctly extract the stock symbol
        
    elif choice == "U.S. Stocks":
        selected_index = st.selectbox("Select an index:", ['DOW JONES', 'S&P 500'])
        stock_options = list(INDICES[selected_index].items())
        stock_names = [f"{name} ({symbol})" for name, symbol in stock_options]
        stock_choice = st.selectbox("Select a stock:", stock_names)
        
        # Correctly extract the stock symbol
        stock_symbol = stock_choice.split('(')[-1].strip(')')  # Correctly extract the stock symbol

    elif choice == "Manual Input":
        stock_symbol = st.text_input("Enter the stock symbol (e.g., AAPL, TSLA):").upper()
    
    if stock_symbol:
        stock_data = fetch_stock_data(stock_symbol)
        st.subheader(f"Current stock data for {stock_symbol}:")
        st.write(stock_data)

        if stock_symbol:
            income_stmt, balance_sheet, cash_flow_stmt = fetch_financial_data(stock_symbol)
            display_financial_data(income_stmt, balance_sheet, cash_flow_stmt)
    else:
        st.warning("Invalid selection. Please try again.")

if __name__ == "__main__":
    main()
