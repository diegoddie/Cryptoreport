import requests
import json
import time
from datetime import datetime
from operator import itemgetter

#API call initialization and JSON data extrapolation

API_KEY = "88c3ce0a-5a46-4b1d-aa6f-fc80b667ec46"
URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

parameters = {
    'start':'1',
    'limit':'100',
    'convert':'USD' 
}

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY,
}

r = requests.get(url=URL, headers=headers, params=parameters).json()

#LOGIC - I initialize a function for each type of data I want displayed in the JSON report

def highest_volume():
    #This function returns a dict that has as key-value pair the crypto symbol with the highest volume recorded in the last 24h and the volume amount
    volume_24h = {}
    for currency in r["data"]:
        volume_24h[currency["symbol"]] = round(currency["quote"]["USD"]["volume_24h"], 2)
    max_value = max(volume_24h.values())
    max_value_with_commas = "{:,}".format(max_value)
    highest_volume_crypto = {list(volume_24h.keys())[list(volume_24h.values()).index(max_value)]: f"{max_value_with_commas} $"}
    return highest_volume_crypto


def performance():
    #This function returns two dicts: one has as key-value pair the 10 crypto with the best performance recorded in the last 24h, the second dict returns the 10 worst.
    performance_24h = {}
    for currency in r["data"]:
        performance_24h[currency["symbol"]] = round(currency["quote"]["USD"]["percent_change_24h"], 2)
    best_performers = dict(sorted(performance_24h.items(), key=itemgetter(1), reverse=True)[:10])
    worst_performers = dict(sorted(performance_24h.items(), key=itemgetter(1), reverse=False)[:10])
    best_worst_10_performers = {
        "Top 10 Performers": best_performers,
        "Worst 10 Performers": worst_performers
    }
    return best_worst_10_performers


def top_20_money_needed():
    #This function returns the amount of money needed to buy one unit of each of the top 20 cryptocurrencies
    prices = {}
    for currency in r["data"]:
        if currency["cmc_rank"] < 21:
            prices[currency["symbol"]] = currency['quote']['USD']['price']
    sum_prices = round(sum(prices.values()), 2)
    return str("{:,}".format(sum_prices)) + "$" 


def top_volume_money_needed():
    #This feature returns the amount of money needed to purchase a unit of all cryptocurrencies whose volume of the last 24 hours exceeds $76,000,000
    VOL = 76000000
    top_volume_prices = {}
    for currency in r["data"]:
        if currency["quote"]["USD"]["volume_24h"] > VOL:
            top_volume_prices[currency["symbol"]] = currency["quote"]["USD"]["price"]
    sum_volume_prices = round(sum(top_volume_prices.values()), 2)
    return str("{:,}".format(sum_volume_prices)) + "$"

def profit_and_loss():
    #This function returns the percentage change you get by buying each of the crypto top20 in yesterday’s day compared to their current value
    yesterday_prices = {}
    today_prices = {}
    amount_bought_yesterday = 0
    amount_worth_today = 0
    for currency in r["data"]:
        if currency["cmc_rank"] < 21:
            yesterday_prices[currency["symbol"]] = currency["quote"]["USD"]["price"]*100/(100 + currency["quote"]["USD"]["percent_change_24h"])
            today_prices[currency["symbol"]] = currency["quote"]["USD"]["price"]
    for value in yesterday_prices.values():
        amount_bought_yesterday += value
    for values in today_prices.values():
        amount_worth_today += values
    return str(round((amount_worth_today - amount_bought_yesterday)/amount_bought_yesterday*100, 2)) + "%"

#generating the json report
new_data = {
        "Highest Volume in the last 24h": highest_volume(),
        "Performance": performance(),
        "Money needed to buy one unit of each of the top 20 crypto": top_20_money_needed(),
        "Money needed to purchase a unit of all cryptocurrencies whose volume of the last 24 hours exceeds $76,000,000": top_volume_money_needed(),
        "Profit and Loss compared to yesterday": profit_and_loss()
    }
while True:
    today = datetime.today().strftime('%Y-%m-%d')
    with open (f"report_{today}.json", "w") as data_file:
        json.dump(new_data, data_file, indent=4)
    minutes = 1440
    seconds = minutes * 60
    time.sleep(seconds)




    





