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
stock.index = pd.to_datetime(stock.index)
stock.columns = ["open", "high", "low", "close", "volume"]
stock = stock.astype(float)
stock = stock.sort_index(ascending=True)

sma1 = 20
sma2 = 40

stock["SMA1"] = stock["close"].rolling(sma1).mean()
stock["SMA2"] = stock["close"].rolling(sma2).mean()


stock.dropna(inplace=True)


stock["Position"] = np.where(stock["SMA1"] > stock["SMA2"], 1, -1)

ax = (
    stock[["close", "SMA1", "SMA2"]].plot(
        secondary_y="Position",
        figsize=(20, 5),
        grid=True,
        title="The simple moving averages of Microsoft (MSFT)",
    ),
    plt.show(),
)
ax.get_legend().set_bbox_to_anchor((0.25, 0.85))
# plt.show()
