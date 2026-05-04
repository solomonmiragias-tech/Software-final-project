import pandas as pd

prices = pd.read_csv("VISA_close.txt", header=None)[0].values

min_price = prices[0]
max_profit = 0

buy_day = 0
sell_day = 0
temp_buy_day = 0

for i in range(1, len(prices)):
    profit = prices[i] - min_price

    if profit > max_profit:
        max_profit = profit
        buy_day = temp_buy_day
        sell_day = i

    if prices[i] < min_price:
        min_price = prices[i]
        temp_buy_day = i

print("Max Profit:", round(max_profit, 2))
print("Buy Day:", buy_day + 1)
print("Sell Day:", sell_day + 1)
