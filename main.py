import sys
from binance import Client
import pandas as pd

import mlTwo
import scalping
import mlOne
import bollinger_bands
import rsi_sma
import plotly.graph_objects as go


api_key = 'kgcF15uxEQiQ6axBDxzUO2XZzUebzvAaDmzVI0JLoMNExwPmOralZ7iON7WZ56gR'
secret_key = 'fHkz7A3ESW7ynD74OPnYDUvRxS70nTJZVzF9et5gIidoO5EpcrZNY0LNMFfxUJM4'
client = Client(api_key, secret_key)


def getminutedata(symbol, interval, lookback):
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback))
    frame = frame.iloc[:, :6]
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)
    return frame


def menu():
    while True:
        cripto_token = input("Kripto para türünü seçiniz: ")
        time_period = input("Zaman paritesini seçiniz: ")
        time_lenght = input("Zaman aralığını seçiniz: ")
        cripto_t = cripto_token + "USDT"
        df = getminutedata(cripto_t, time_period, time_lenght)
        kf = client.get_klines(symbol=cripto_t, interval='1m')

        while True:
            print("[1] Seçilen Kripto Paranın Grafiğini Göster")
            print("[2] Seçilen kripto para üzerinde bollinger bands algoritmasını gerçekleştir")
            print("[3] Seçilen kripto para üzerinde rsi_sma algoritmasını uygula")
            print("[4] Seçilen kripto para üzerinde scalping algoritmasını uygula")
            print("[5] Seçilen kripto para üzerinde 1.makine öğrenmesi algoritması uygula")
            print("[6] Seçilen kripto para üzerinde 2.makine öğrenmesi algoritması uygula")
            print("[7] Farklı bir kripto para veya parite seç")
            print("[0] Sistemden çık")

            desicion = int(input("Lütfen işlem numarasını seçiniz: "))

            if desicion == 1:
                fig = go.Figure(data=[go.Candlestick(x=df.index,
                                                     open=df['Open'],
                                                     high=df['High'],
                                                     low=df['Low'],
                                                     close=df['Close'])])
                fig.show()
                print(df)
            elif desicion == 2:
                bollinger_bands.bb_backtest(df)
            elif desicion == 3:
                rsi_sma.bt_rsisma(df)
            elif desicion == 4:
                scalping.scalping(df)
            elif desicion == 5:
                mlOne.ml_one(df)
            elif desicion == 6:
                mlTwo.ml_two(kf)
            elif desicion == 7:
                break
            elif desicion == 0:
                sys.exit()
            else:
                print("Yanlış bir tuşa bastınız")
                continue


menu()
