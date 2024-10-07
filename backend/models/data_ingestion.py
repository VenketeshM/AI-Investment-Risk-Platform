# scripts/data_ingestion.py

import requests# type: ignore
import yfinance as yf # type: ignore
import pandas as pd # type: ignore

# Set your API key
API_KEY = 'crvvnkpr01qrbtrl5g00crvvnkpr01qrbtrl5g0g'

# Predefined stock symbols for Indian and American Indices
INDICES = {
    'NIFTY 50': {
    'Reliance Industries': 'RELIANCE.NS',
    'Tata Consultancy Services': 'TCS.NS',
    'HDFC Bank': 'HDFCBANK.NS',
    'Infosys': 'INFY.NS',
    'ICICI Bank': 'ICICIBANK.NS',
    'Larsen & Toubro': 'LT.NS',
    'State Bank of India': 'SBIN.NS',
    'Bharti Airtel': 'BHARTIARTL.NS',
    'Kotak Mahindra Bank': 'KOTAKBANK.NS',
    'Hindustan Unilever': 'HINDUNILVR.NS',
    'ITC': 'ITC.NS',
    'HDFC': 'HDFC.NS',
    'Bajaj Finance': 'BAJFINANCE.NS',
    'Axis Bank': 'AXISBANK.NS',
    'Asian Paints': 'ASIANPAINT.NS',
    'Adani Ports': 'ADANIPORTS.NS',
    'Tata Motors': 'TATAMOTORS.NS',
    'Sun Pharmaceutical': 'SUNPHARMA.NS',
    'Mahindra & Mahindra': 'M&M.NS',
    'Power Grid Corporation': 'POWERGRID.NS',
    'Titan Company': 'TITAN.NS',
    'UltraTech Cement': 'ULTRACEMCO.NS',
    'NTPC': 'NTPC.NS',
    'Nestle India': 'NESTLEIND.NS',
    'Dr. Reddy\'s Laboratories': 'DRREDDY.NS',
    'Maruti Suzuki India': 'MARUTI.NS',
    'Grasim Industries': 'GRASIM.NS',
    'Wipro': 'WIPRO.NS',
    'UPL': 'UPL.NS',
    'Coal India': 'COALINDIA.NS',
    'Divi\'s Laboratories': 'DIVISLAB.NS',
    'HCL Technologies': 'HCLTECH.NS',
    'Tech Mahindra': 'TECHM.NS',
    'Shree Cement': 'SHREECEM.NS',
    'Cipla': 'CIPLA.NS',
    'Bajaj Finserv': 'BAJAJFINSV.NS',
    'Tata Consumer Products': 'TATACONSUM.NS',
    'Eicher Motors': 'EICHERMOT.NS',
    'Hero MotoCorp': 'HEROMOTOCO.NS',
    'Britannia Industries': 'BRITANNIA.NS',
    'IndusInd Bank': 'INDUSINDBK.NS',
    'Indian Oil Corporation': 'IOC.NS',
    'JSW Steel': 'JSWSTEEL.NS',
    'BPCL': 'BPCL.NS',
    'ONGC': 'ONGC.NS',
    'SBI Life Insurance': 'SBILIFE.NS',
    'Tata Steel': 'TATASTEEL.NS',
    'Adani Green Energy': 'ADANIGREEN.NS',
    'Adani Enterprises': 'ADANIENT.NS',
    'Apollo Hospitals': 'APOLLOHOSP.NS'
    },
    'BANK NIFTY': {
    'HDFC Bank': 'HDFCBANK.NS',
    'ICICI Bank': 'ICICIBANK.NS',
    'State Bank of India': 'SBIN.NS',
    'Kotak Mahindra Bank': 'KOTAKBANK.NS',
    'Axis Bank': 'AXISBANK.NS',
    'IndusInd Bank': 'INDUSINDBK.NS',
    'Bandhan Bank': 'BANDHANBNK.NS',
    'Federal Bank': 'FEDERALBNK.NS',
    'IDFC First Bank': 'IDFCFIRSTB.NS',
    'Punjab National Bank': 'PNB.NS',
    'RBL Bank': 'RBLBANK.NS',
    'AU Small Finance Bank': 'AUBANK.NS'
    },
    'FINNIFTY': {
    'HDFC': 'HDFC.NS',
    'Bajaj Finserv': 'BAJAJFINSV.NS',
    'HDFC Life': 'HDFCLIFE.NS',
    'SBI Life Insurance': 'SBILIFE.NS',
    'ICICI Lombard': 'ICICIGI.NS',
    'Kotak Mahindra Bank': 'KOTAKBANK.NS',
    'HDFC Bank': 'HDFCBANK.NS',
    'Axis Bank': 'AXISBANK.NS',
    'ICICI Bank': 'ICICIBANK.NS',
    'Bajaj Finance': 'BAJFINANCE.NS',
    'State Bank of India': 'SBIN.NS',
    'Max Financial Services': 'MFSL.NS',
    'PNB Housing Finance': 'PNBHOUSING.NS',
    'Cholamandalam Investment': 'CHOLAFIN.NS',
    'IDFC First Bank': 'IDFCFIRSTB.NS'
    },
    'SENSEX': {
    'Reliance Industries': 'RELIANCE.NS',
    'HDFC Bank': 'HDFCBANK.NS',
    'HDFC': 'HDFC.NS',
    'Tata Consultancy Services': 'TCS.NS',
    'Infosys': 'INFY.NS',
    'ICICI Bank': 'ICICIBANK.NS',
    'Hindustan Unilever': 'HINDUNILVR.NS',
    'Bharti Airtel': 'BHARTIARTL.NS',
    'ITC': 'ITC.NS',
    'Kotak Mahindra Bank': 'KOTAKBANK.NS',
    'Asian Paints': 'ASIANPAINT.NS',
    'Tata Steel': 'TATASTEEL.NS',
    'Maruti Suzuki': 'MARUTI.NS',
    'Nestle India': 'NESTLEIND.NS',
    'Bajaj Finance': 'BAJFINANCE.NS',
    'Axis Bank': 'AXISBANK.NS',
    'Mahindra & Mahindra': 'M&M.NS',
    'Larsen & Toubro': 'LT.NS',
    'State Bank of India': 'SBIN.NS',
    'NTPC': 'NTPC.NS',
    'Sun Pharmaceutical Industries': 'SUNPHARMA.NS',
    'Power Grid Corporation': 'POWERGRID.NS',
    'Wipro': 'WIPRO.NS',
    'UltraTech Cement': 'ULTRACEMCO.NS',
    'Titan Company': 'TITAN.NS',
    'Dr. Reddy\'s Laboratories': 'DRREDDY.NS',
    'Tech Mahindra': 'TECHM.NS',
    'JSW Steel': 'JSWSTEEL.NS',
    'IndusInd Bank': 'INDUSINDBK.NS',
    'Grasim Industries': 'GRASIM.NS',
    'Coal India': 'COALINDIA.NS',
    'Cipla': 'CIPLA.NS',
    'Bajaj Finserv': 'BAJAJFINSV.NS',
    'Tata Consumer Products': 'TATACONSUM.NS',
    'Eicher Motors': 'EICHERMOT.NS',
    'Hero MotoCorp': 'HEROMOTOCO.NS',
    'Britannia Industries': 'BRITANNIA.NS',
    'Adani Ports': 'ADANIPORTS.NS',
    'Apollo Hospitals': 'APOLLOHOSP.NS'
    },
    'DOW JONES': {
    'Apple Inc.': 'AAPL',
    'Microsoft Corp.': 'MSFT',
    'Visa Inc.': 'V',
    'Johnson & Johnson': 'JNJ',
    'Walmart Inc.': 'WMT',
    'UnitedHealth Group': 'UNH',
    'Boeing Co.': 'BA',
    'Coca-Cola Co.': 'KO',
    'Goldman Sachs Group': 'GS',
    'Intel Corp.': 'INTC',
    '3M Co.': 'MMM',
    'American Express Co.': 'AXP',
    'Procter & Gamble Co.': 'PG',
    'Home Depot Inc.': 'HD',
    'Cisco Systems Inc.': 'CSCO',
    'McDonald\'s Corp.': 'MCD',
    'Disney (Walt) Co.': 'DIS',
    'Verizon Communications Inc.': 'VZ',
    'IBM Corp.': 'IBM',
    'Nike Inc.': 'NKE',
    'Dow Inc.': 'DOW',
    },
    'S&P 500': {
        '3M Company': 'MMM',
        'A. O. Smith Corporation': 'AOS',
        'Abbott Laboratories': 'ABT',
        'AbbVie Inc.': 'ABBV',
        'Accenture plc': 'ACN',
        'Activision Blizzard, Inc.': 'ATVI',
        'ADP': 'ADP',
        'Adobe Inc.': 'ADBE',
        'Advanced Micro Devices, Inc.': 'AMD',
        'Aflac Incorporated': 'AFL',
        'Air Products and Chemicals, Inc.': 'APD',
        'Akamai Technologies, Inc.': 'AKAM',
        'Alaska Air Group, Inc.': 'ALK',
        'Albemarle Corporation': 'ALB',
        'Align Technology, Inc.': 'ALGN',
        'Altria Group, Inc.': 'MO',
        'Amazon.com, Inc.': 'AMZN',
        'Amcor plc': 'AMCR',
        'AMD': 'AMD',
        'Ameren Corporation': 'AEE',
        'American Airlines Group Inc.': 'AAL',
        'American Electric Power Company, Inc.': 'AEP',
        'American Express Company': 'AXP',
        'American International Group, Inc.': 'AIG',
        'American Tower Corporation': 'AMT',
        'American Water Works Company, Inc.': 'AWK',
        'Ameriprise Financial, Inc.': 'AMP',
        'AmerisourceBergen Corporation': 'ABC',
        'Aon plc': 'AON',
        'APA Corporation': 'APA',
        'Apple Inc.': 'AAPL',
        'Applied Materials, Inc.': 'AMAT',
        'Archer-Daniels-Midland Company': 'ADM',
        'Arthur J. Gallagher & Co.': 'AJG',
        'Assurant, Inc.': 'AIZ',
        'AT&T Inc.': 'T',
        'Atmos Energy Corporation': 'ATO',
        'Autodesk, Inc.': 'ADSK',
        'AvalonBay Communities, Inc.': 'AVB',
        'Avery Dennison Corporation': 'AVY',
        'Baker Hughes Company': 'BKR',
        'Ball Corporation': 'BALL',
        'Bank of America Corporation': 'BAC',
        'Baxter International Inc.': 'BAX',
        'Becton, Dickinson and Company': 'BDX',
        'Berkshire Hathaway Inc.': 'BRK.B',
        'Best Buy Co., Inc.': 'BBY',
        'Bio-Rad Laboratories, Inc.': 'BIO',
        'BlackRock, Inc.': 'BLK',
        'Boeing Company (The)': 'BA',
        'Booking Holdings Inc.': 'BKNG',
        'BorgWarner Inc.': 'BWA',
        'Boston Properties, Inc.': 'BXP',
        'Boston Scientific Corporation': 'BSX',
        'Bristol-Myers Squibb Company': 'BMY',
        'Broadcom Inc.': 'AVGO',
        'C.H. Robinson Worldwide, Inc.': 'CHRW',
        'Cadence Design Systems, Inc.': 'CDNS',
        'Caesars Entertainment, Inc.': 'CZR',
        'Camden Property Trust': 'CPT',
        'Campbell Soup Company': 'CPB',
        'Capital One Financial Corporation': 'COF',
        'Cardinal Health, Inc.': 'CAH',
        'CarMax, Inc.': 'KMX',
        'Carnival Corporation': 'CCL',
        'Carrier Global Corporation': 'CARR',
        'Catalent, Inc.': 'CTLT',
        'Caterpillar Inc.': 'CAT',
        'Cboe Global Markets, Inc.': 'CBOE',
        'CBRE Group, Inc.': 'CBRE',
        'CDW Corporation': 'CDW',
        'Celanese Corporation': 'CE',
        'Centene Corporation': 'CNC',
        'Ceridian HCM Holding Inc.': 'CDAY',
        'CF Industries Holdings, Inc.': 'CF',
        'Charles River Laboratories International, Inc.': 'CRL',
        'Charles Schwab Corporation (The)': 'SCHW',
        'Charter Communications, Inc.': 'CHTR',
        'Chevron Corporation': 'CVX',
        'Chipotle Mexican Grill, Inc.': 'CMG',
        'Chubb Limited': 'CB',
        'Cigna Corporation': 'CI',
        'Cincinnati Financial Corporation': 'CINF',
        'Cintas Corporation': 'CTAS',
        'Citigroup Inc.': 'C',
        'Citizens Financial Group, Inc.': 'CFG',
        'The Clorox Company': 'CLX',
        'The Coca-Cola Company': 'KO',
        'Cognizant Technology Solutions Corporation': 'CTSH',
        'Colgate-Palmolive Company': 'CL',
        'Comcast Corporation': 'CMCSA',
        'Comerica Incorporated': 'CMA',
        'Conagra Brands, Inc.': 'CAG',
        'ConocoPhillips': 'COP',
        'Consolidated Edison, Inc.': 'ED',
        'Constellation Brands, Inc.': 'STZ',
        'CoStar Group, Inc.': 'CSGP',
        'Corteva, Inc.': 'CTVA',
        'Coty Inc.': 'COTY',
        'Crown Castle Inc.': 'CCI',
        'CSX Corporation': 'CSX',
        'Cummins Inc.': 'CMI',
        'CVS Health Corporation': 'CVS',
        'D.R. Horton, Inc.': 'DHI',
        'Danaher Corporation': 'DHR',
        'Darden Restaurants, Inc.': 'DRI',
        'Deere & Company': 'DE',
        'Delta Air Lines, Inc.': 'DAL',
        'Devon Energy Corporation': 'DVN',
        'Dexcom, Inc.': 'DXCM',
        'Digital Realty Trust, Inc.': 'DLR',
        'Discover Financial Services': 'DFS',
        'Dish Network Corporation': 'DISH',
        'Disney (The Walt Disney Company)': 'DIS',
        'Dollar General Corporation': 'DG',
        'Dollar Tree, Inc.': 'DLTR',
        'Dominion Energy, Inc.': 'D',
        "Domino's Pizza, Inc.": 'DPZ',
        'DTE Energy Company': 'DTE',
        'DuPont de Nemours, Inc.': 'DD',
        'DXC Technology Company': 'DXC',
        'Eastman Chemical Company': 'EMN',
        'Eaton Corporation plc': 'ETN',
        'eBay Inc.': 'EBAY',
        'Ecolab Inc.': 'ECL',
        'Edison International': 'EIX',
        'Edwards Lifesciences Corporation': 'EW',
        'Electronic Arts Inc.': 'EA',
        'Elevance Health, Inc.': 'ELV',
        'Emerson Electric Co.': 'EMR',
        'Enphase Energy, Inc.': 'ENPH',
        'Entergy Corporation': 'ETR',
        'EQT Corporation': 'EQT',
        'Equifax Inc.': 'EFX',
        'Equinix, Inc.': 'EQIX',
        'Equity Residential': 'EQR',
        'Essex Property Trust, Inc.': 'ESS',
        'Exelon Corporation': 'EXC',
        'Expedia Group, Inc.': 'EXPE',
        'Extra Space Storage Inc.': 'EXR',
        'Exxon Mobil Corporation': 'XOM',
        'F5, Inc.': 'FFIV',
        'FactSet Research Systems Inc.': 'FDS',
        'Fastenal Company': 'FAST',
        'Federal Realty Investment Trust': 'FRT',
        'FedEx Corporation': 'FDX',
        'Fidelity National Information Services, Inc.': 'FIS',
        'Fifth Third Bancorp': 'FITB',
        'First Republic Bank': 'FRC',
        'First Solar, Inc.': 'FSLR',
        'FirstEnergy Corp.': 'FE',
        'FISERV, Inc.': 'FISV',
        'Fleetcor Technologies, Inc.': 'FLT',
        'Fluor Corporation': 'FLR',
        'Foot Locker, Inc.': 'FL',
        'Fortinet, Inc.': 'FTNT',
        'Fortive Corporation': 'FTV',
        'Fox Corporation': 'FOXA',
        'Franklin Templeton Investments': 'BEN',
        'Freeport-McMoRan Inc.': 'FCX',
        'Garmin Ltd.': 'GRMN',
        'Garrett Motion Inc.': 'GTX',
        'Generac Holdings Inc.': 'GNRC',
        'General Dynamics Corporation': 'GD',
        'General Electric Company': 'GE',
        'General Mills, Inc.': 'GIS',
        'General Motors Company': 'GM',
        'Gilead Sciences, Inc.': 'GILD',
        'Globe Life Inc.': 'GL',
        'Goldman Sachs Group, Inc. (The)': 'GS',
        'Halliburton Company': 'HAL',
        'Hartford Financial Services Group, Inc. (The)': 'The Hartford',
        'Hasbro, Inc.': 'HAS',
        'HCA Healthcare, Inc.': 'HCA',
        'Harris Corporation': 'HII',
        'Hewlett Packard Enterprise Company': 'HPE',
        'Hilton Worldwide Holdings Inc.': 'HLT',
        'Hologic, Inc.': 'HOLX',
        'Home Depot, Inc. (The)': 'HD',
        'Honeywell International Inc.': 'HON',
        'Hormel Foods Corporation': 'HRL',
        'Host Hotels & Resorts, Inc.': 'HST',
        'Howmet Aerospace Inc.': 'HWM',
        'HP Inc.': 'HPQ',
        'Humana Inc.': 'HUM',
        'Huntington Bancshares Incorporated': 'HBAN',
        'IPG Photonics Corporation': 'IPGP',
        'Idexx Laboratories, Inc.': 'IDXX',
        'Illinois Tool Works Inc.': 'ITW',
        'Illumina, Inc.': 'ILMN',
        'Incyte Corporation': 'INCY',
        'Ingersoll Rand Inc.': 'IR',
        'Intel Corporation': 'INTC',
        'Intercontinental Exchange, Inc.': 'ICE',
        'International Business Machines Corporation': 'IBM',
        'International Flavors & Fragrances Inc.': 'IFF',
        'International Paper Company': 'IP',
        'Interpublic Group of Companies, Inc. (The)': 'IPG',
        'Intuit Inc.': 'INTU',
        'Intuitive Surgical, Inc.': 'ISRG',
        'Invesco Ltd.': 'IVZ',
        'IPG Photonics Corporation': 'IPGP',
        'J.B. Hunt Transport Services, Inc.': 'JBHT',
        'Jacobs Engineering Group Inc.': 'J',
        'JPMorgan Chase & Co.': 'JPM',
        'KeyCorp': 'KEY',
        'Keysight Technologies, Inc.': 'KEYS',
        'Kroger Co.': 'KR',
        'L3Harris Technologies, Inc.': 'LHX',
        'Lamb Weston Holdings, Inc.': 'LW',
        'Larsen & Toubro Limited': 'LT',
        'Las Vegas Sands Corp.': 'LVS',
        'Leidos Holdings, Inc.': 'LDOS',
        'Lincoln National Corporation': 'LNC',
        'Lockheed Martin Corporation': 'LMT',
        'Loews Corporation': 'L',
        'LyondellBasell Industries N.V.': 'LYB',
        'Marathon Petroleum Corporation': 'MPC',
        'MarketAxess Holdings Inc.': 'MKTX',
        'Marriott International, Inc.': 'MAR',
        'Marsh & McLennan Companies, Inc.': 'MMC',
        'Martin Marietta Materials, Inc.': 'MLM',
        'Masonite International Corporation': 'DOOR',
        'Mastercard Incorporated': 'MA',
        'McCormick & Company, Incorporated': 'MKC',
        "McDonald's Corporation": 'MCD',
        'McKesson Corporation': 'MCK',
        'Medtronic plc': 'MDT',
        'Merck & Co., Inc.': 'MRK',
        'MetLife, Inc.': 'MET',
        'Mettler-Toledo International Inc.': 'MTD',
        'MGM Resorts International': 'MGM',
        'Microchip Technology Incorporated': 'MCHP',
        'Micron Technology, Inc.': 'MU',
        'Microsoft Corporation': 'MSFT',
        'Mid-America Apartment Communities, Inc.': 'MAA',
        'Moelis & Company': 'MC',
        'Mosaic Company (The)': 'MOS',
        'Motorola Solutions, Inc.': 'MSI',
        'Nasdaq, Inc.': 'NDAQ',
        'NetApp, Inc.': 'NTAP',
        'Netflix, Inc.': 'NFLX',
        'NVIDIA Corporation': 'NVDA',
        'Noble Energy, Inc.': 'NBL',
        'Norfolk Southern Corporation': 'NSC',
        'Northrop Grumman Corporation': 'NOC',
        'NortonLifeLock Inc.': 'NLOK',
        'Novartis AG': 'NVS',
        'NRG Energy, Inc.': 'NRG',
        'NVIDIA Corporation': 'NVDA',
        'O\'Reilly Automotive, Inc.': 'ORLY',
        'Occidental Petroleum Corporation': 'OXY',
        'Oklahoma Gas & Electric': 'OGE',
        'Old Dominion Freight Line, Inc.': 'ODFL',
        'Omnicom Group Inc.': 'OMC',
        'Oracle Corporation': 'ORCL',
        "O'Reilly Automotive, Inc.": 'ORLY',
        'Parker-Hannifin Corporation': 'PH',
        'Paychex, Inc.': 'PAYX',
        'PayPal Holdings, Inc.': 'PYPL',
        'Pentair plc': 'PNR',
        'PepsiCo, Inc.': 'PEP',
        'PerkinElmer, Inc.': 'PKI',
        'Pfizer Inc.': 'PFE',
        'Philip Morris International Inc.': 'PM',
        'Phillips 66': 'PSX',
        'Prudential Financial, Inc.': 'PRU',
        'Public Service Enterprise Group Incorporated': 'PEG',
        'PulteGroup, Inc.': 'PHM',
        'Qorvo, Inc.': 'QRVO',
        'Raytheon Technologies Corporation': 'RTX',
        'Regeneron Pharmaceuticals, Inc.': 'REGN',
        'Republic Services, Inc.': 'RSG',
        'ResMed Inc.': 'RMD',
        'Robert Half International Inc.': 'RHI',
        'Rockwell Automation, Inc.': 'ROK',
        'Rollins, Inc.': 'ROL',
        'Ross Stores, Inc.': 'ROST',
        'Royal Caribbean Group': 'RCL',
        'S&P Global Inc.': 'SPGI',
        'Salesforce, Inc.': 'CRM',
        'Seagate Technology Holdings plc': 'STX',
        'Second Sight Medical Products, Inc.': 'EYES',
        'Sempra Energy': 'SRE',
        'ServiceNow, Inc.': 'NOW',
        'Sherwin-Williams Company (The)': 'SHW',
        'Simon Property Group, Inc.': 'SPG',
        'Skyworks Solutions, Inc.': 'SWKS',
        'S&P Global Inc.': 'SPGI',
        'Snap Inc.': 'SNAP',
        'SolarEdge Technologies, Inc.': 'SEDG',
        'Southern Company (The)': 'SO',
        'Southwest Airlines Co.': 'LUV',
        'Stanley Black & Decker, Inc.': 'SWK',
        'Starbucks Corporation': 'SBUX',
        'State Street Corporation': 'STT',
        'Stryker Corporation': 'SYK',
        'Synchrony Financial': 'SYF',
        'Sysco Corporation': 'SYY',
        'T. Rowe Price Group, Inc.': 'TROW',
        'Take-Two Interactive Software, Inc.': 'TTWO',
        'Tapestry, Inc.': 'TPR',
        'Target Corporation': 'TGT',
        'Tata Consultancy Services': 'TCS',
        'Teradyne, Inc.': 'TER',
        'Tesla, Inc.': 'TSLA',
        'Texas Instruments Incorporated': 'TXN',
        'Thermo Fisher Scientific Inc.': 'TMO',
        'The Travelers Companies, Inc.': 'TRV',
        'The Union Bank of Switzerland': 'UBS',
        'The Walt Disney Company': 'DIS',
        'Thermo Fisher Scientific Inc.': 'TMO',
        'Thomson Reuters Corporation': 'TRI',
        'T-Mobile US, Inc.': 'TMUS',
        'Toronto-Dominion Bank (The)': 'TD',
        'Tractor Supply Company': 'TSCO',
        'Truist Financial Corporation': 'TFC',
        'Twitter, Inc.': 'TWTR',
        'Tyler Technologies, Inc.': 'TYL',
        'Uber Technologies, Inc.': 'UBER',
        'U.S. Bancorp': 'USB',
        'Union Pacific Corporation': 'UNP',
        'United Airlines Holdings, Inc.': 'UAL',
        'United Parcel Service, Inc.': 'UPS',
        'UnitedHealth Group Incorporated': 'UNH',
        'Universal Health Services, Inc.': 'UHS',
        'Unum Group': 'UNM',
        'Valero Energy Corporation': 'VLO',
        'Varian Medical Systems, Inc.': 'VAR',
        'Verisk Analytics, Inc.': 'VRSK',
        'Verizon Communications Inc.': 'VZ',
        'Vertex Pharmaceuticals Incorporated': 'VRTX',
        'VF Corporation': 'VFC',
        'ViacomCBS Inc.': 'VIAC',
        'Viatris Inc.': 'VTRS',
        'Visa Inc.': 'V',
        'Vistra Corp.': 'VST',
        'VMware, Inc.': 'VMW',
        'Walmart Inc.': 'WMT',
        'Walt Disney Company (The)': 'DIS',
        'Waste Management, Inc.': 'WM',
        'Wayfair Inc.': 'W',
        'Westrock Company': 'WRK',
        'Weyerhaeuser Company': 'WY',
        'Whirlpool Corporation': 'WHR',
        'Williams Companies, Inc. (The)': 'WMB',
        'Wells Fargo & Company': 'WFC',
        'Western Digital Corporation': 'WDC',
        'Westlake Chemical Corporation': 'WLK',
        'Weyerhaeuser Company': 'WY',
        'Wynn Resorts, Limited': 'WYNN',
        'Xcel Energy Inc.': 'XEL',
        'Xilinx, Inc.': 'XLNX',
        'Xperi Holding Corporation': 'XPER',
        'Yum! Brands, Inc.': 'YUM',
        'Zebra Technologies Corporation': 'ZBRA',
        'Zions Bancorporation, National Association': 'ZION'
    }
}


# def fetch_stock_data(symbol):
#     """Fetch stock data from Yahoo Finance."""
#     print(f"Fetching data for symbol: {symbol}")  # Print the symbol for debugging
#     try:
#         stock = yf.Ticker(symbol)
#         data = stock.history(period="1d")  # Fetching the latest day's data
#         if not data.empty:
#             # Formatting the output for better readability
#             output = data.iloc[-1].to_dict()
#             formatted_output = "\n".join([f"{key}: {value:.2f}" for key, value in output.items()])
#             return formatted_output
#         else:
#             print(f"No data found for {symbol}.")
#             return None
#     except Exception as e:
#         print(f"Error fetching data: {e}")
#         return None
    
def fetch_stock_data(symbol):
    """Fetch stock data from Yahoo Finance."""
    print(f"Fetching data for symbol: {symbol}")  # Print the symbol for debugging
    try:
        stock = yf.Ticker(symbol)
        stock_info = stock.info
        data = stock.history(period="1d")  # Fetching the latest day's data
        if not data.empty:
            # Formatting the output for better readability
            output = data.iloc[-1].to_dict()
            formatted_output = "\n".join([f"{key}: {value:.2f}" for key, value in output.items() if isinstance(value, (int, float))])
            print(formatted_output)  # Print the formatted output for better visibility
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
            print(f"No data found for {symbol}.")
            return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def fetch_financial_data(symbol):
    """Fetch income statement, balance sheet, and cash flow statement from Yahoo Finance."""
    print(f"Fetching financial data for symbol: {symbol}")
    try:
        stock = yf.Ticker(symbol)
        
        # Fetch financial statements
        income_statement = stock.financials
        balance_sheet = stock.balance_sheet
        cash_flow = stock.cashflow
        
        return income_statement, balance_sheet, cash_flow
    except Exception as e:
        print(f"Error fetching financial data: {e}")
        return None, None, None

def format_to_crores(df):
    """Convert financial figures to crores and format the DataFrame."""
    if df is not None and not df.empty:
        # Convert to crores (1 crore = 10,000,000)
        df_crores = df / 10_000_000
        # Round to two decimal places
        df_crores = df_crores.round(2)
        return df_crores
    else:
        return df

def calculate_metrics(income, balance, cash_flow):
    """Calculate financial metrics like ROE, ROC, EBITDA, Debt to Equity, Profit Margin, ROA, and Current Ratio."""
    metrics = {}
    
    try:
        # Ensure the necessary fields exist for each calculation
        if 'Net Income' in income.index and 'Total Equity' in balance.index:
            # ROE = Net Income / Shareholder's Equity
            net_income = income.loc['Net Income'].iloc[0]
            shareholders_equity = balance.loc['Total Equity'].iloc[0]
            metrics['ROE (%)'] = (net_income / shareholders_equity) * 100
        
        if 'EBITDA' in income.index and 'Interest Expense' in income.index and 'Total Assets' in balance.index and 'Current Liabilities' in balance.index:
            # ROC = (Net Income + Interest Expense) / (Total Assets - Current Liabilities)
            net_income = income.loc['Net Income'].iloc[0]
            interest_expense = income.loc['Interest Expense'].iloc[0]
            total_assets = balance.loc['Total Assets'].iloc[0]
            current_liabilities = balance.loc['Current Liabilities'].iloc[0]
            metrics['ROC (%)'] = ((net_income + interest_expense) / (total_assets - current_liabilities)) * 100
        
        if 'EBITDA' in income.index:
            # EBITDA = Earnings Before Interest, Taxes, Depreciation, and Amortization
            ebitda = income.loc['EBITDA'].iloc[0]
            metrics['EBITDA (Crores)'] = ebitda / 10_000_000  # Convert to crores

        if 'Total Debt' in balance.index and 'Total Equity' in balance.index:
            # Debt to Equity Ratio = Total Debt / Total Equity
            total_debt = balance.loc['Total Debt'].iloc[0]
            total_equity = balance.loc['Total Equity'].iloc[0]
            metrics['Debt to Equity Ratio'] = total_debt / total_equity
        
        if 'Net Income' in income.index and 'Total Revenue' in income.index:
            # Net Profit Margin = Net Income / Total Revenue
            net_income = income.loc['Net Income'].iloc[0]
            total_revenue = income.loc['Total Revenue'].iloc[0]
            metrics['Net Profit Margin (%)'] = (net_income / total_revenue) * 100
        
        if 'Net Income' in income.index and 'Total Assets' in balance.index:
            # Return on Assets (ROA) = Net Income / Total Assets
            net_income = income.loc['Net Income'].iloc[0]
            total_assets = balance.loc['Total Assets'].iloc[0]
            metrics['ROA (%)'] = (net_income / total_assets) * 100
        
        if 'Current Assets' in balance.index and 'Current Liabilities' in balance.index:
            # Current Ratio = Current Assets / Current Liabilities
            current_assets = balance.loc['Current Assets'].iloc[0]
            current_liabilities = balance.loc['Current Liabilities'].iloc[0]
            metrics['Current Ratio'] = current_assets / current_liabilities
        
    except Exception as e:
        print(f"Error calculating metrics: {e}")
    
    return metrics


def display_financial_data(income, balance, cash_flow):
    """Display formatted financial data along with calculated metrics."""
    print("\n### Income Statement ###")
    if income is not None and not income.empty:
        income_formatted = format_to_crores(income)
        print(income_formatted.to_string())
    else:
        print("No Income Statement data available.")
    
    print("\n### Balance Sheet ###")
    if balance is not None and not balance.empty:
        balance_formatted = format_to_crores(balance)
        print(balance_formatted.to_string())
    else:
        print("No Balance Sheet data available.")
    
    print("\n### Cash Flow Statement ###")
    if cash_flow is not None and not cash_flow.empty:
        cash_flow_formatted = format_to_crores(cash_flow)
        print(cash_flow_formatted.to_string())
    else:
        print("No Cash Flow Statement data available.")
    
    # Calculate and display metrics
    metrics = calculate_metrics(income, balance, cash_flow)
    if metrics:
        print("\n### Financial Metrics ###")
        for metric, value in metrics.items():
            if isinstance(value, float):
                print(f"{metric}: {value:.2f}")
            else:
                print(f"{metric}: {value}")
    else:
        print("No financial metrics available.")



def display_dropdown_menu():
    """Display the dropdown menu for selecting stock options."""
    print("Select an option:")
    print("1. Indian Stocks (Nifty 50, Bank Nifty, FinNifty, Sensex)")
    print("2. U.S. Stocks (Dow Jones, S&P 500)")
    print("3. Manual Input")
    choice = input("Enter your choice (1, 2 or 3): ")

    if choice == '1':
        print("\nSelect an index:")
        print("1. Nifty 50")
        print("2. Bank Nifty")
        print("3. FinNifty")
        print("4. Sensex")
        index_choice = input("Enter the index number (1, 2, 3, or 4): ")

        index_map = {
            '1': 'NIFTY 50',
            '2': 'BANK NIFTY',
            '3': 'FINNIFTY',
            '4': 'SENSEX'
        }

        selected_index = index_map.get(index_choice)
        if selected_index:
            print(f"\nAvailable stocks in {selected_index}:")
            for i, (name, symbol) in enumerate(INDICES[selected_index].items(), 1):
                print(f"{i}. {name} ({symbol})")
            stock_choice = int(input("Select a stock by entering the corresponding number: "))
            stock_symbol = list(INDICES[selected_index].values())[stock_choice - 1]
        else:
            print("Invalid index choice, please try again.")
            return display_dropdown_menu()

    elif choice == '2':
        print("\nSelect a U.S. index:")
        print("1. Dow Jones")
        print("2. S&P 500")
        index_choice = input("Enter the index number (1, 2): ")

        index_map = {
            '1': 'DOW JONES',
            '2': 'S&P 500'
        }

        selected_index = index_map.get(index_choice)
        if selected_index:
            print(f"\nAvailable stocks in {selected_index}:")
            for i, (name, symbol) in enumerate(INDICES[selected_index].items(), 1):
                print(f"{i}. {name} ({symbol})")
            stock_choice = int(input("Select a stock by entering the corresponding number: "))
            stock_symbol = list(INDICES[selected_index].values())[stock_choice - 1]
        else:
            print("Invalid index choice, please try again.")
            return display_dropdown_menu()

    elif choice == '3':
        stock_symbol = input("Enter the stock symbol (e.g., AAPL, TSLA): ").upper()

    else:
        print("Invalid choice, please try again.")
        return display_dropdown_menu()

    return stock_symbol

def main():
    """Main function to run the stock data fetching and displaying process."""
    stock_symbol = display_dropdown_menu()
    
    stock_data = fetch_stock_data(stock_symbol)
    income, balance, cash_flow = fetch_financial_data(stock_symbol)

    display_financial_data(income, balance, cash_flow)

if __name__ == "__main__":
    main()
