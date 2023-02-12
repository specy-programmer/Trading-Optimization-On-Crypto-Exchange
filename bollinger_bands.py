import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def bollinger_bands(df, desicion):
    buys = []
    sells = []
    open_pos = False
    for i in range(len(df)):
        if df.Lower[i] > df.Close[i]:
            if open_pos == False:
                buys.append(i)
                open_pos = True
        elif df.Upper[i] < df.Close[i]:
            if open_pos:
                sells.append(i)
                open_pos = False

    if desicion == 'buys':
        return buys
    else:
        return sells


def bb_backtest(df):
    df['SMA'] = df.Close.rolling(window=20).mean()
    df['stddev'] = df.Close.rolling(window=20).std()
    df['Upper'] = df.SMA + 2 * df.stddev
    df['Lower'] = df.SMA - 2 * df.stddev
    df['Buy_signal'] = np.where(df.Lower > df.Close, True, False)
    df['Sell_signal'] = np.where(df.Upper < df.Close, True, False)
    df = df.dropna()
    plt.plot(df[['Close', 'SMA', 'Upper', 'Lower']])
    plt.scatter(df.index[df.Buy_signal], df[df.Buy_signal].Close, marker='^', color='g')
    plt.scatter(df.index[df.Sell_signal], df[df.Sell_signal].Close, marker='v', color='r')
    plt.fill_between(df.index, df.Upper, df.Lower, color='grey', alpha=0.3)
    plt.legend(df[['Close', 'SMA', 'Upper', 'Lower']])
    plt.show()
    merged = pd.concat([df.iloc[bollinger_bands(df, 'buys')].Close, df.iloc[bollinger_bands(df, 'sells')].Close],
                       axis=1)
    merged.columns = ['Buys', 'Sells']
    totalprofit = merged.shift(-1).Sells - merged.Buys
    relprofits = ((merged.shift(-1).Sells - merged.Buys) / merged.Buys) * 100
    relprofits = relprofits.dropna()
    print(relprofits)
    print(f'Mean profit: {relprofits.mean()}')
