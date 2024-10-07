import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Dashboard = ({ stockSymbol }) => {
    const [stockData, setStockData] = useState(null);
    const [financialData, setFinancialData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null); // Added for error handling

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true); // Start loading
            setError(null); // Reset error state

            try {
                const stockResponse = await axios.get(`/api/stock/${stockSymbol}`);
                const financialResponse = await axios.get(`/api/financials/${stockSymbol}`);

                setStockData(stockResponse.data);
                setFinancialData(financialResponse.data);
            } catch (error) {
                console.error('Error fetching data:', error);
                setError('Failed to fetch data.'); // Set error message
            } finally {
                setLoading(false); // Stop loading
            }
        };

        fetchData();
    }, [stockSymbol]);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div style={{ color: 'red' }}>{error}</div>; // Display error message
    }

    return (
        <div>
            <h2>Stock Data for {stockSymbol}</h2>
            {stockData ? (
                <pre>{JSON.stringify(stockData, null, 2)}</pre>
            ) : (
                <p>No stock data available.</p>
            )}
            <h2>Financial Data</h2>
            {financialData ? (
                <pre>{JSON.stringify(financialData, null, 2)}</pre>
            ) : (
                <p>No financial data available.</p>
            )}
        </div>
    );
};

export default Dashboard;
