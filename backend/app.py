# backend/app.py

from flask import Flask, jsonify, request
import yfinance as yf
from portfolio_management import get_stock_price  # Import your existing functions
from data_ingestion import INDICES  # Assuming this is a dict with stock data

app = Flask(__name__)

# Endpoint to get the stock price
@app.route('/api/stock_price/<string:symbol>', methods=['GET'])
def stock_price(symbol):
    try:
        price = get_stock_price(symbol)
        if price is not None:
            return jsonify({"symbol": symbol, "price": price}), 200
        else:
            return jsonify({"error": "No data available"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to get all available stocks from a specific index
@app.route('/api/stocks/<string:index>', methods=['GET'])
def get_stocks(index):
    if index in INDICES:
        return jsonify(INDICES[index]), 200
    else:
        return jsonify({"error": "Index not found"}), 404

# Endpoint to manage the portfolio (add, remove, list)
@app.route('/api/portfolio', methods=['POST', 'GET'])
def portfolio():
    if request.method == 'POST':
        # Logic to add stocks to the portfolio
        # This would typically involve updating a database or in-memory storage
        stock_data = request.json
        return jsonify({"message": "Stock added to portfolio!"}), 201
    elif request.method == 'GET':
        # Logic to return the current portfolio
        return jsonify({"portfolio": []})  # Replace with actual portfolio data

if __name__ == '__main__':
    app.run(debug=True)
