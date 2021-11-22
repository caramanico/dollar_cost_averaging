import sys
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
import os

class stock():
    def __init__(self, symbol, expectedAllocation, shares, price):
        self.symbol = symbol
        self.expectedAllocation = expectedAllocation
        self.shares = shares
        self.price = price

yf.pdr_override()

NDIGITS = 4
availableCash = int(input("Cash Available: ") or 0)
portfolio = int(input("Portfolio name: 1. Long Term. 2. Short Term: ") or 0)
print("\n")

portfolioValue = 0
stocks = []
startDate = dt.datetime(2021,11,19)
now = dt.datetime.now()

sys.stdout = open(os.devnull, 'w') # Disable the print

# Load data and calculate portfolio value
if (portfolio == 2):
	file = pd.read_csv('short_term.csv')
else:
	file = pd.read_csv('long_term.csv')

for i in file.index:
	price = pdr.get_data_yahoo(file["symbol"][i], startDate, now)['Adj Close'][-1]
	stocks.append(
		stock(file["symbol"][i],
			file["allocation"][i],
			file["shares"][i],
			price)
	)
	portfolioValue += file["shares"][i] * price

sys.stdout = sys.__stdout__ # Enable the print

# Calculate current allocation for each stock
for stock in stocks:
	stock.currentAllocation = stock.shares * stock.price / portfolioValue

# Calculate the portfolio value after buying additional shares
newPortfolioValue = portfolioValue + availableCash

totalAllocationDiff = 0

# Calculate future allocation with the new portfolio value
for stock in stocks:
	stock.futureAllocation = stock.shares * stock.price / newPortfolioValue
	if (stock.futureAllocation < stock.expectedAllocation):
		totalAllocationDiff += stock.expectedAllocation - stock.futureAllocation

# Calculate amount to invest in each stock
data = []
for stock in stocks:
	if (stock.futureAllocation < stock.expectedAllocation):
		stock.amountToInvest = (stock.expectedAllocation - stock.futureAllocation) / totalAllocationDiff * availableCash
		stock.sharesToBuy = stock.amountToInvest / stock.price
	else:
		stock.amountToInvest = 0
		stock.sharesToBuy = 0

	data.append([
		stock.symbol,
		str(stock.shares),
		str(round(stock.price, NDIGITS)),
		str(round(stock.expectedAllocation * 100, NDIGITS)) + "%",
		str(round(stock.currentAllocation * 100, NDIGITS)) + "%",
		"$" + str(round(stock.amountToInvest, NDIGITS)),
		str(round(stock.amountToInvest / stock.price, NDIGITS)),
		str(round((stock.price * stock.shares + stock.amountToInvest) / newPortfolioValue * 100, NDIGITS)) + "%"
	])

print(pd.DataFrame(data,
	columns = ['Stock', '# of shares', 'Price',
				'Expected allocation', 'Current allocation',
				'New investment ($)', 'New investment (# of shares)',
				'New allocation']))

print("\nNew portfolio value: $" + str(round(newPortfolioValue, 2))
	+ " (" + str(round((newPortfolioValue/portfolioValue - 1) * 100, 2)) + "% growth)\n")

