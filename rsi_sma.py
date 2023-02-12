import ta
import pandas as pd
import numpy as np


def bt_rsisma(df):
    df['SMA200'] = ta.trend.sma_indicator(df.Close, window=200)
    df['RSI'] = ta.momentum.rsi(df.Close, window=10)
    df['Signal'] = np.where((df.Close > df.SMA200) & (df.RSI < 30), True, False)
    Buying_dates = []
    Selling_dates = []

    for i in range(len(df)):
        if df.Signal.iloc[i]:
            Buying_dates.append(df.iloc[i + 1].name)
            for j in range(1, 11):
                if df['RSI'].iloc[i + j] > 40:
                    Selling_dates.append(df.iloc[i + j + 1].name)
                    break
                elif j == 10:
                    Selling_dates.append(df.iloc[i + j + 1].name)


    frame = pd.DataFrame({'Buying_dates': Buying_dates, 'Selling_dates': Selling_dates})
    actualtrades = frame[frame.Buying_dates > frame.Selling_dates.shift(1)]
    actualtrades = frame[:1].append(actualtrades)
    profits = df.loc[actualtrades.Selling_dates].Open.values - df.loc[actualtrades.Buying_dates].Open.values
    relprofits = ((df.loc[actualtrades.Selling_dates].Open.values - df.loc[actualtrades.Buying_dates].Open.values) /
                  df.loc[actualtrades.Buying_dates].Open.values) * 100
    print(actualtrades)
    print(relprofits)
    print(f"Real profit: {relprofits.mean()}")
