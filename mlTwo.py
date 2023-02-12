import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from keras.layers.core import Dense
from keras.layers import LSTM
from keras.models import Sequential


def ml_two(kf):
    price = np.array([float(kf[i][4]) for i in range(500)])
    time = np.array([int(kf[i][0]) for i in range(500)])

    t = np.array([datetime.fromtimestamp(time[i] / 1000).strftime('%H:%M:%S') for i in range(500)])

    plt.figure(figsize=(8, 5))
    plt.xlabel('Time Step')
    plt.ylabel('Bitcoin Price $')
    plt.plot(price)

    timeframe = pd.DataFrame({'Time': t, 'Price $BTC': price})
    price = price.reshape(500, 1)

    scaler = StandardScaler()
    scaler.fit(price[:374])
    StandardScaler(copy=True, with_mean=True, with_std=True)
    price = scaler.transform(price)
    df = pd.DataFrame(price.reshape(100, 5), columns=['First', 'Second', 'Third', 'Fourth', 'Target'])

    x_train = df.iloc[:74, :4]
    y_train = df.iloc[:74, -1]

    x_test = df.iloc[75:99, :4]
    y_test = df.iloc[75:99, -1]
    x_train = np.array(x_train)
    y_train = np.array(y_train)
    x_test = np.array(x_test)
    y_test = np.array(y_test)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    x_train.shape, x_test.shape
    ((74, 4, 1), (24, 4, 1))
    model = Sequential()

    model.add(LSTM(20, return_sequences=True, input_shape=(4, 1)))
    model.add(LSTM(40, return_sequences=False))
    model.add(Dense(1, activation='linear'))
    model.compile(loss='mse', optimizer='rmsprop')
    model.fit(x_train, y_train, batch_size=5, epochs=100)

    y_pred = model.predict(x_test)
    y_test = y_test.reshape(-1, 1)
    plt.figure(figsize=[8, 5])
    plt.xlabel('Time Step')
    plt.ylabel('Price')
    plt.plot(scaler.inverse_transform(y_test), label='True')
    plt.plot(scaler.inverse_transform(y_pred), label='Prediction')
    plt.legend()
    plt.show()
