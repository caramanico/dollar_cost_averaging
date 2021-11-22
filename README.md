# Dollar Cost Averaging Python script
Script to calculate how many shares to buy each month.

Based on a stock portfolio and the cash available to buy new shares, the script returns how many shares of each stock you need to buy to balance the portfolio and meet the expected allocation.

The cash available is an input of the script, and the CSV contains the symbol, the expected percentage allocation, and the current number of shares for each stock.

## Setup
* Python version: 3
* pip install pandas
* pip install pandas_datareader
* pip install yfinance
* Create the csv file (long_term.csv and/or short_term.csv): symbol,allocation,shares

## Execute
* python3 dollar_cost_averaging.py

