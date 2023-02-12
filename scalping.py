import pandas_ta as ta
import numpy as np
import plotly.graph_objects as go
from backtesting import Strategy
from backtesting import Backtest


def scalping(df):
    df = df[df['Volume'] != 0]
    df.isna().sum()

    df["EMA50"] = ta.ema(df.Close, length=50)
    df["EMA100"] = ta.ema(df.Close, length=100)
    df["EMA150"] = ta.ema(df.Close, length=150)

    backrollingN = 10
    df['slopeEMA50'] = df['EMA50'].diff(periods=1)
    df['slopeEMA50'] = df['slopeEMA50'].rolling(window=backrollingN).mean()

    df['slopeEMA100'] = df['EMA100'].diff(periods=1)
    df['slopeEMA100'] = df['slopeEMA100'].rolling(window=backrollingN).mean()

    df['slopeEMA150'] = df['EMA150'].diff(periods=1)
    df['slopeEMA150'] = df['slopeEMA150'].rolling(window=backrollingN).mean()

    conditions = [
        ((df['EMA50'] < df['EMA100']) & (df['EMA100'] < df['EMA150']) & (df['slopeEMA50'] < 0) & (
                    df['slopeEMA100'] < 0) & (df['slopeEMA150'] < 0)),
        ((df['EMA50'] > df['EMA100']) & (df['EMA100'] > df['EMA150']) & (df['slopeEMA50'] > 0) & (
                    df['slopeEMA100'] > 0) & (df['slopeEMA150'] > 0))
    ]
    choices = [1, 2]
    df['EMAsignal'] = np.select(conditions, choices, default=0)

    TotSignal = [0] * len(df)
    for row in range(0, len(df)):
        TotSignal[row] = 0
        if df.EMAsignal[row] == 1 and df.Open[row] > df.EMA50[row] and df.Close[row] < df.EMA50[row]:
            TotSignal[row] = 1
        if df.EMAsignal[row] == 2 and df.Open[row] < df.EMA50[row] and df.Close[row] > df.EMA50[row]:
            TotSignal[row] = 2

    df['TotSignal'] = TotSignal
    df.dropna(inplace=True)

    def pointpos(x):
        if x['TotSignal'] == 1:
            return x['High'] + 1e-3
        elif x['TotSignal'] == 2:
            return x['Low'] - 1e-3
        else:
            return np.nan

    df['pointpos'] = df.apply(lambda row: pointpos(row), axis=1)

    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close']),
                          go.Scatter(x=df.index, y=df.EMA50, line=dict(color='orange', width=1), name="EMA50"),
                          go.Scatter(x=df.index, y=df.EMA100, line=dict(color='blue', width=1), name="EMA100"),
                          go.Scatter(x=df.index, y=df.EMA150, line=dict(color='red', width=1), name="EMA150")])

    fig.add_scatter(x=df.index, y=df['pointpos'], mode="markers",
                    marker=dict(size=5, color="MediumPurple"),
                    name="Signal")
    fig.show()

    df['ATR'] = ta.atr(df.High, df.Low, df.Close, length=10)

    def SIGNAL():
        return df.TotSignal

    class MyStrat(Strategy):
        initsize = 0.10
        mysize = initsize

        def init(self):
            super().init()
            self.signal1 = self.I(SIGNAL)

        def next(self):
            super().next()
            slatr = 2 * self.data.ATR[-1]
            TPSLRatio = 1.5

            if self.signal1 == 2 and len(self.trades) == 0:
                sl1 = self.data.Close[-1] - slatr
                tp1 = self.data.Close[-1] + slatr * TPSLRatio
                self.buy(sl=sl1, tp=tp1, size=self.mysize)

            elif self.signal1 == 1 and len(self.trades) == 0:
                sl1 = self.data.Close[-1] + slatr
                tp1 = self.data.Close[-1] - slatr * TPSLRatio
                self.sell(sl=sl1, tp=tp1, size=self.mysize)

    bt = Backtest(df, MyStrat, cash=10000, margin=1 / 10, commission=.00)
    stat = bt.run()
    print(stat)
    bt.plot(show_legend=False)
