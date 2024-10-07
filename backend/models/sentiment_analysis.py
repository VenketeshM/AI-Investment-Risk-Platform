import requests # type: ignore
from textblob import TextBlob# type: ignore
import yfinance as yf  # type: ignore
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup # type: ignore
from nltk.sentiment.vader import SentimentIntensityAnalyzer # type: ignore
import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore

# Import functions from the data_ingestion module
from data_ingestion import display_dropdown_menu, fetch_stock_data

finvix_url = 'https://finviz.com/quote.ashx?t='

def plot_daily_sentiment(news_df):
    """Plot daily average sentiment from the news DataFrame."""
    # Group by date and calculate the average sentiment
    daily_sentiment = news_df.groupby('date')['compound'].mean().reset_index()

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=daily_sentiment, x='date', y='compound', marker='o')
    plt.title('Daily Average Sentiment')
    plt.xlabel('Date')
    plt.ylabel('Average Sentiment Score')
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.show()

def plot_historical_stock_data(stock_symbol):
    """Fetch historical stock data and plot it."""
    # Fetch historical stock data for the past year
    stock_data = yf.download(stock_symbol, start="2023-01-01", end="2024-01-01")  # Change the date range as needed
    stock_data['Close'].plot(figsize=(12, 6), label='Close Price', color='blue')
    plt.title(f'Historical Stock Prices for {stock_symbol}')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.xticks(rotation=45)
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Use the dropdown to select a stock symbol
    stock_symbol = display_dropdown_menu()

    # Fetch stock data
    stock_data = fetch_stock_data(stock_symbol)
    print(f"\nCurrent stock data for {stock_symbol}: {stock_data}")

    news_tables = {}

    # Dictionary to store parsed data and sentiment
    parsed_data = []

    # Initialize VADER sentiment analyzer
    vader = SentimentIntensityAnalyzer()

    # Fetch news from Finviz
    URL = finvix_url + stock_symbol
    REQ = Request(url=URL, headers={'user-agent': 'my-app'})

    try:
        response = urlopen(REQ)
        html = response.read()  # Read the response content
        soup = BeautifulSoup(html, 'lxml')  # Specify the parser

        # Find the news table
        news_table = soup.find(id='news-table')
        if news_table:
            news_tables[stock_symbol] = news_table

            # Process news rows
            stock_rows = news_table.findAll('tr')
            for row in stock_rows:
                columns = row.findAll('td')

                if len(columns) == 2:
                    news_date_time = columns[0].get_text().strip()
                    news_headline = columns[1].get_text().strip()

                    # Split the date and time, handle both cases (with and without time)
                    date, time = "", ""
                    if ' ' in news_date_time:
                        date_time_parts = news_date_time.split(' ')
                        if len(date_time_parts) == 2:
                            date, time = date_time_parts
                        else:
                            date = date_time_parts[0]
                    else:
                        date = news_date_time

                    # Store the data in a dictionary
                    parsed_data.append({
                        'ticker': stock_symbol,
                        'date': date,
                        'time': time,
                        'headline': news_headline
                    })

                    # Print in the format: Ticker | Date | Time | Headline
                    print(f"{stock_symbol} | {date} | {time} | {news_headline}")

        else:
            print("No news table found.")

    except Exception as e:
        print(f"Error fetching data from Finviz: {e}")

    # Convert parsed data into a DataFrame
    news_df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'headline'])

    # Apply sentiment analysis on the 'headline' column using VADER
    f = lambda headline: vader.polarity_scores(headline)['compound']
    news_df['compound'] = news_df['headline'].apply(f)
    news_df['date'] = pd.to_datetime(news_df.date).dt.date
    
    print("\nNews Data with Sentiment:")
    print(news_df)

    # Optional: Save the DataFrame to a CSV file for further use
    news_df.to_csv(f'{stock_symbol}_news_sentiment.csv', index=False)

    # Plot daily sentiment
    plot_daily_sentiment(news_df)

    # Plot historical stock data
    plot_historical_stock_data(stock_symbol)
