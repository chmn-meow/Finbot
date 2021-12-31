import os
import pandas as pd
import pandas_datareader as pdr
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import requests
import json
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
api_key = str(os.environ.get("API"))

plt.style.use("seaborn")
mpl.rcParams["font.family"] = "serif"


def get_tsd(symbol, api):
    response = requests.get(
        f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api}"
    )
    alphadict = json.loads(response.text)
    return alphadict["Time Series (Daily)"]


stock = pd.DataFrame(get_tsd("MSFT", api_key)).T
# print(stock.info())
# print(type(stock.index))
stock.index = pd.to_datetime(stock.index)
# print(type(stock.index))
# print(stock["close"]) - creates key error...
stock.columns = ["open", "high", "low", "close", "volume"]
stock = stock.astype(float)
sample = stock.sample(10)
# print(sample)
summary = stock.describe()
# print(summary)
# stock["close"].plot(figsize=(20, 5), title="Microsoft (MSFT) daily closing prices"), plt.show()
stock = stock.sort_index(ascending=True)

stock["SMA10"] = stock["close"].rolling(10).mean()
stock["SMA20"] = stock["close"].rolling(20).mean()
# print(stock.head())

stock.dropna(inplace=True)
# print(stock.head())
# stock[["close", "SMA10", "SMA20"]].plot(figsize=(20, 5),grid=True,title="The 10 and 20 day simple moving averages of Microsoft (MSFT)",), plt.show()

signal = pd.DataFrame()
signal["crossover"] = stock["SMA10"] - stock["SMA20"]
# print(signal.tail())
stock = stock.join(signal, how="left")
# print(stock.tail())
signal["close-close"] = stock["close"].diff()
# print(signal.head())
signal.dropna(inplace=True)
quality = (signal["crossover"] > 0) & (signal["close-close"] > 0) | (
    signal["crossover"] < 0
) & (signal["close-close"] < 0)
# print(quality.head())
quality = quality.astype(int)
# print(quality.head())
proportion_correct = quality.sum() / quality.count()
# print(proportion_correct)
information_coefficient = 2 * proportion_correct - 1
# print(information_coefficient)
# print(signal.corr(method="spearman"))
